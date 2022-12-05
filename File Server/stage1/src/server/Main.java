package server;

import java.io.*;
import java.util.*;

public class Main {

    public static void main(String[] args) throws IOException {
        Storage storage = new Storage();
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            String[] tokens = reader.readLine().split("\\s");
            String command = tokens[0];
            if ("exit".equals(command)) break;
            String filename = tokens[1];
            switch (command) {
                case "add": {
                    System.out.printf(storage.add(filename) ? "The file %s added successfully\n" :
                            "Cannot add the file %s\n", filename);
                    break;
                }
                case "get": {
                    System.out.printf(storage.get(filename) ? "The file %s was sent\n" :
                            "The file %s not found\n", filename);
                    break;
                }
                case "delete": {
                    System.out.printf(storage.delete(filename) ? "The file %s was deleted\n" :
                            "The file %s not found\n", filename);
                    break;
                }
            }
        }
    }
}

class Storage {

    Set<String> files = new HashSet<>();

    boolean add(String file) {
        return checkFileName(file) && files.add(file);
    }
    boolean get(String file) {
        return checkFileName(file) && files.contains(file);
    }
    boolean delete(String file) {
        return checkFileName(file) && files.remove(file);
    }
    boolean checkFileName(String filename) {
        return filename.matches("file\\d0?");
    }
}