/**
 * Created by Frank on 3/12/16.
 */


//import org.apache.tika.cli.TikaCLI;
import org.apache.tika.exception.TikaException;
//import org.apache.tika.io.TikaInputStream;
import org.apache.tika.metadata.Metadata;
//import org.apache.tika.metadata.serialization.JsonMetadataList;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
//import org.apache.tika.parser.RecursiveParserWrapper;
import org.apache.tika.sax.BodyContentHandler;
//import org.xml.sax.ContentHandler;
import org.xml.sax.SAXException;
import org.apache.tika.parser.geo.topic.GeoParser;
import org.apache.tika.parser.geo.topic.GeoParserConfig;
import org.apache.tika.parser.Parser;

import org.json.simple.JSONObject;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

import static java.util.Objects.*;
//import java.net.URL;

public class YaoGeoTopicParser {
    final String gazetteer = "src/main/java/org/apache/tika/parser/geo/topic/model/allCountries.txt";

    final String folderName = "geo-topic-parser-folder-output";
    public ArrayList<String> arrayList = new ArrayList<>();

    public HashSet<String> fileSet = new HashSet<>();
    public int startIndex = 0;
    public Integer endIndex;
    public static void main(String[] args) throws IOException, TikaException, SAXException {
        YaoGeoTopicParser yaoParser = new YaoGeoTopicParser();
        if (args.length >= 1) {
            yaoParser.startIndex = Integer.decode(args[0]);
            System.out.println(new StringBuffer("starting at index: ").append(yaoParser.startIndex).toString());
        }
        if (args.length >= 2) {
            yaoParser.endIndex = Integer.decode(args[1]);
            System.out.println(new StringBuffer("ending at index: ").append(yaoParser.endIndex).toString());
        }
        yaoParser.preProcess();

        yaoParser.readIndexFile("/Users/Frank/PycharmProjects/599assignment1/geo-topic-parser-folder/geo-topic-all-files.txt");
        yaoParser.run();
    }

    public void readIndexFile(String string) {
        try (BufferedReader br = new BufferedReader(new FileReader(string))) {
            String line;
            while ((line = br.readLine()) != null) {
                this.arrayList.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void preProcess() {
        File directory = new File(folderName);
        if (!directory.exists()) {
            boolean result = false;
            try {
                result = directory.mkdir();

            } catch (SecurityException e) {
                e.printStackTrace();
            } finally {
                if (!result) {
                    System.err.println("Error: Folder didn't create!");
                }
            }
        }
        try {
            Files.walk(Paths.get(directory.getAbsolutePath())).forEach(filePath -> {
                String[] parts = filePath.getFileName().toString().split("\\.");
                if (parts.length > 0) {
                    this.fileSet.add(parts[0]);
                }

            });
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void run() {
        ArrayList<String> arrayList = new ArrayList<>();
//        arrayList.add("/Users/Frank/Desktop/fulldump/raw-dataset/gov/911/www/32F91475FDAEBD5162E0098CECC9193AD0BAC8681E3CCAFC7295877BE0D5571A");
//        arrayList.add("/Users/Frank/Desktop/fulldump/raw-dataset/gov/911/www/B4F2131A435E04591D9BF1D03E8C8B9BB3CC5773DD2CDB294D07887A42731F67");
//        arrayList.add("/Users/Frank/Desktop/fulldump/raw-dataset/gov/abilityone/www/1C0C1634C7D0ACC3ED18FC0E368BA0ECBB9BEC0E00AC792640E0C87CFCD57C2D");
        if (this.arrayList != null) {
            //arrayList.addAll(this.arrayList);
            arrayList = this.arrayList;
        }
        List<TaskObject> taskList = new ArrayList<>();
        int endIndex;
        if (this.endIndex == null) {
            endIndex = arrayList.size();
        } else {
            endIndex = this.endIndex < arrayList.size() ? this.endIndex : arrayList.size();
        }
        for (int i = startIndex; i < endIndex; i++) {
            if (i % 1000 == 0) {
                System.out.println(i);
            }
            String filepath = arrayList.get(i);
            if (this.fileSet.contains(Paths.get(filepath).getFileName().toString())) {
                continue;
            }
            taskList.add(new TaskObject(filepath));
        }

        taskList.parallelStream().forEach(TaskObject::run);
        //taskList.stream().forEach(TaskObject::run);
    }


    public class TaskObject {
        private String filepath;
        private final String folderName = "geo-topic-parser-folder-output";
        public TaskObject(String string) {
            this.filepath = string;
        }
        private Parser geoparser = new GeoParser();
        private final String nerPath = "/Users/Frank/src/location-ner-model/org/apache/tika/parser/geo/topic/en-ner-location.bin";

        public void run() {
            String text = null;
            try {
                text = this.extractText(new FileInputStream(filepath));
            } catch (IOException e) {
                e.printStackTrace();
            }
            if (text == null) {
                return;
            }
            Metadata metadata = this.parseGeoTopic(text.replaceAll("(?m)^[ \t]*\r?\n", ""));
            Path path = Paths.get(filepath);
            try {
                this.dumpMetadata(metadata, this.folderName, path.getFileName().toString());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public String extractText(InputStream stream) throws IOException {

            AutoDetectParser parser = new AutoDetectParser();
            BodyContentHandler handler = new BodyContentHandler();
            Metadata metadata = new Metadata();
            //InputStream stream = getResourceAsStream("/Users/Frank/Downloads/OPT-Workshop-2015-2016.pdf";
            try {
                parser.parse(stream, handler, metadata);
                return handler.toString();
            } catch (SAXException | TikaException e) {
                e.printStackTrace();
            } finally {
                stream.close();
            }
            return null;
        }

        public Metadata parseGeoTopic(String text) {

            Metadata metadata = new Metadata();
            ParseContext context = new ParseContext();
            GeoParserConfig config = new GeoParserConfig();
            //config.setGazetterPath(gazetteer);
            config.setNERModelPath(this.nerPath);
            context.set(GeoParserConfig.class, config);

            InputStream inputStream = null;
            try {
                inputStream = new ByteArrayInputStream(text.getBytes("UTF-8"));
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }

            try {
                geoparser.parse(inputStream, new BodyContentHandler(), metadata, context);
            } catch (IOException | SAXException | TikaException e) {
                e.printStackTrace();
            }

            //System.out.println(metadata.toString());

            return metadata;
        }

        public boolean dumpMetadata(Metadata metadata, String folder, String filename) throws IOException {
            if (metadata == null) {
                return false;
            }
            if (metadata.size() == 0) {
                return true;
            }
            HashMap<String, String> map = new HashMap<>();
            for (String key : metadata.names()) {
                map.put(key, metadata.get(key));
            }
            JSONObject json = new JSONObject(map);

            FileWriter fileWriter = null;
            try {
                fileWriter = new FileWriter(folder + '/' + filename + ".json");
            } catch (IOException e) {
                e.printStackTrace();
            }
            String result = json.toJSONString();
            if (result != null && fileWriter != null) {
                fileWriter.write(result);
                fileWriter.flush();
                fileWriter.close();
            }

            return true;
        }
    }
}
