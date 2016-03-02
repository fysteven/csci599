/**
 * Created by Frank on 2/29/16.
 */
import java.util.HashMap;
import java.util.LinkedList;

public class KellyFileManager {
    public HashMap<String, String> fileMap = new HashMap<String, String>();
    public HashMap<String, Integer> duplicateFileMap = new HashMap<String, Integer>();

    public boolean checkExistence(String filename) {
        if (fileMap.containsKey(filename)) {
            if (duplicateFileMap.containsKey(filename)) {
                duplicateFileMap.put(filename, 0);
            } else {
                duplicateFileMap.put(filename, duplicateFileMap.get(filename) + 1);
            }

            return true;
        } else {
            return false;
        }
    }

    public void addFiles(LinkedList<String> filenameList) {
        for (int i = 0; i < filenameList.size(); i++) {
            fileMap.put(filenameList.get(0), "1");
        }
    }

    public void addFile(String filename) {
        fileMap.put(filename, "1");
    }
}
