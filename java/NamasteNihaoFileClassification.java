/**
 * Created by Frank on 3/1/16.
 */

import com.uwyn.jhighlight.fastutil.Hash;
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
    public HashMap<String, HashMap<String, Integer>> typeFileMap = new HashMap<>();
    public HashMap<String, HashMap<String, Integer>> oldTypeFileMap = new HashMap<>();
    public HashMap<String, HashMap<String, Integer>> typeCountMap = new HashMap<>();
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

        for (String string : args) {
            System.out.println(string);
        }

        fileClassification.prepareProcessing();

        ArrayList<String> filepaths = fileClassification.getAllFilepaths(Arrays.copyOfRange(args, 0, args.length));
        fileClassification.identifyFileType(filepaths);
        fileClassification.dumpAllMapsToJSON(System.getProperty("user.dir") + "/output");
    }

    public void prepareProcessing() {
        this.typeCountMap.put("old", new HashMap<>());
        this.typeCountMap.put("new", new HashMap<>());
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
                        if (!currentFileMap.containsKey(file.getName())) {
                            if (typeCountMap.get("old").containsKey(file.getParentFile().getName())) {
                                HashMap<String, Integer> countMap = typeCountMap.get("old");
                                countMap.put(file.getParentFile().getName(), countMap.get(file.getParentFile().getName()) + 1);
                            } else {
                                typeCountMap.get("old").put(file.getParentFile().getName(), 1);
                            }
                        }
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

    public void identifyFileType(ArrayList<String> filepaths) throws IOException {
        System.out.println("Start identifying");

        Tika tika = new Tika();
        filepaths.forEach((item) -> {
                    File file = new File(item);
                    String fileType = null;
                    try {
                        fileType = tika.detect(file);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    if (fileTypeMap.containsKey(file.getName())) {
                        if (duplicateMap.containsKey(file.getName())) {
                            duplicateMap.put(file.getName(), duplicateMap.get(file.getName()) + 1);
                        } else {
                            duplicateMap.put(file.getName(), 1);
                        }
                    } else {
                        fileTypeMap.put(file.getName(), fileType);
                        if (!typeFileMap.containsKey(fileType)) {
                            typeFileMap.put(fileType, new HashMap<String, Integer>());
                        }

                        if (typeCountMap.get("new").containsKey(fileType)) {
                            HashMap<String, Integer> countMap = typeCountMap.get("new");
                            countMap.put(fileType, countMap.get(fileType) + 1);
                        } else {
                            typeCountMap.get("new").put(fileType, 1);
                        }

                        HashMap<String, Integer> fileMap = (HashMap<String, Integer>) typeFileMap.get(fileType);
                        fileMap.put(file.getName(), 1);
                    }
                }
        );



    }

    @SuppressWarnings("unchecked")
    public void dumpAllMapsToJSON(String jsonFilePath) throws IOException {
        System.out.println("Start dump all maps to json");
        JSONObject json = new JSONObject(typeCountMap);

        /*
        JSONObject json2 = new JSONObject();
        JSONObject json3 = new JSONObject();
        JSONObject json4 = new JSONObject();

        json.put("oldTypeFile", this.oldTypeFileMap);
        json2.put("typeFile", this.typeFileMap);
        json3.put("fileType", this.fileTypeMap);
        json4.put("duplicate", this.duplicateMap);
        */
        System.out.println("Writing to JSON files");

        FileWriter fileWriter = new FileWriter(jsonFilePath + "typeCount.json");
        fileWriter.write(json.toJSONString());
        fileWriter.flush();
        fileWriter.close();
        /*
        FileWriter fileWriter2 = new FileWriter(jsonFilePath + "2.json");
        fileWriter2.write(json2.toJSONString());
        fileWriter2.flush();
        fileWriter2.close();

        FileWriter fileWriter3 = new FileWriter(jsonFilePath + "3.json");
        fileWriter3.write(json3.toJSONString());
        fileWriter3.flush();
        fileWriter3.close();

        FileWriter fileWriter4 = new FileWriter(jsonFilePath + "4.json");
        fileWriter4.write(json4.toJSONString());
        fileWriter4.flush();
        fileWriter4.close();
        */
    }
}
