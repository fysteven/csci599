/**
 * Created by Frank on 3/1/16.
 */

import org.apache.tika.Tika;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.stream.Stream;

import org.json.simple.JSONObject;

public class NamasteNihaoFileClassification {
    public static String cwd = System.getProperty("user.dir") + "/";
    public HashMap<String, String> fileTypeMap = new HashMap<>();
    public HashMap<String, HashMap> typeFileMap = new HashMap<>();
    public HashMap<String, HashMap> oldTypeFileMap = new HashMap<>();
    public HashMap<String, Integer> duplicateMap = new HashMap<>();
/*
    public static void main(String[] args) throws Exception {
        String dirAnalyse = args[0];
        Tika tika = new Tika();
        File dir = new File(dirAnalyse);
        String[] paths = dir.list();
        for (String fName : paths) {
            String curLocation = cwd + dirAnalyse + "/" + fName;
            //System.out.println("curLocation : " + curLocation);
            File curfile = new File(curLocation);
            String fileType = tika.detect(curfile);
            System.out.print("fileType : " + fileType);
            System.out.println(" : " + fName);
        }
    }
*/
    public static  void main(String[] args) throws Exception {
        NamasteNihaoFileClassification fileClassification = new NamasteNihaoFileClassification();
        //System.out.println(args);
        ArrayList<String> filepaths = fileClassification.getAllFilepaths(Arrays.copyOfRange(args, 0, args.length));
        fileClassification.identifyFileType(filepaths);
        fileClassification.dumpAllMapsToJSON(System.getProperty("user.dir") + "/nmstOutput.json");
    }

    public ArrayList<String> getAllFilepaths(String[] args) {
        System.out.println("Start getting all file paths");

        ArrayList<String> fileList = new ArrayList<>();

        for (String folderString : args) {

            try (Stream<Path> paths = Files.walk(Paths.get(folderString))) {
                //File file1 = new File(folderString);

                paths.forEach((path) -> {
                    File file = new File(path.toString());
                    if (!file.isDirectory() && !file.getName().equals(".DS_Store")) {
                        fileList.add(path.toString());

                        if (!oldTypeFileMap.containsKey(file.getParentFile().getName())) {
                            oldTypeFileMap.put(file.getParentFile().getName(), new HashMap<String, Integer>());
                        }

                        HashMap<String, Integer> currentFileMap = oldTypeFileMap.get(file.getParentFile().getName());
                        currentFileMap.put(file.getName(), 1);
                    }

                });
            } catch (IOException e) {
                e.printStackTrace();
            }
            /*
            File folder = new File(folderString);

            if (!oldTypeFileMap.containsKey(folder.getName())) {
                oldTypeFileMap.put(folder.getName(), new HashMap<String, Integer>());
            }
            HashMap<String, Integer> currentFileMap = oldTypeFileMap.get(folder.getName());
            for (String path : folder.list()) {
                fileList.add(path);
                File file = new File(path);
                currentFileMap.put(file.getName(), 1);
            }
            */
        }
        return fileList;
    }

    public void identifyFileType(ArrayList<String> filepaths) {
        System.out.println("Start identifying");

        Tika tika = new Tika();

        filepaths.forEach((item) -> {
                    File file = new File(item);
                    String fileType = tika.detect(item);
                    if (fileTypeMap.containsKey(file.getName())) {
                        if (duplicateMap.containsKey(file.getName())) {
                            duplicateMap.put(file.getName(), duplicateMap.get(file.getName()) + 1);
                        } else {
                            duplicateMap.put(file.getName(), 1);
                        }
                    } else {
                        fileTypeMap.put(file.getName(), fileType);
                        if (!typeFileMap.containsKey(fileType)) {
                            HashMap<String, Integer> fileMap = new HashMap<String, Integer>();
                            typeFileMap.put(fileType, fileMap);
                        }
                        HashMap<String, Integer> fileMap = (HashMap<String, Integer>) typeFileMap.get(fileType);
                        fileMap.put(file.getName(), 1);
                    }
                }
        );


    }

    public void dumpAllMapsToJSON(String jsonFilePath) throws IOException {
        System.out.println("Start dump all maps to json");
        JSONObject json = new JSONObject();
        json.put("oldTypeFile", this.oldTypeFileMap);
        json.put("typeFile", this.typeFileMap);
        json.put("fileType", this.fileTypeMap);
        json.put("duplicate", this.duplicateMap);

        FileWriter fileWriter = new FileWriter(jsonFilePath);
        fileWriter.write(json.toJSONString());
        fileWriter.flush();
        fileWriter.close();
    }
}
