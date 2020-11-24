import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;

class WordInfo {

	  public String word; 
	  public int weight; 
	  public int value;
	  public Integer importance;
	  
	  public WordInfo(String word, int weight, int value, int importance) { 
	    this.word = word; 
	    this.weight = weight; 
	    this.value = value;
	    this.importance = importance;
	  }   
}

public class tagging {

		private static BufferedReader reader;
		private static FileWriter writer;
		private static HashMap<String, WordInfo> map = new HashMap<>();
		
		public static void main(String[] args) {
			try {
				
				reader = new BufferedReader(new FileReader("outfile.txt"));
				File outputFile = new File("weights.txt");
				writer = new FileWriter(outputFile);
				
				//get the first line of the text document containing the values input by the user
				ArrayList<String> values = new ArrayList<String>();
				String firstLine;
				if((firstLine = reader.readLine()) != null) {
					firstLine = firstLine.toLowerCase();
					String[] valuesArray = firstLine.split(" ");
					for(String elem: valuesArray) {
						values.add(elem);
					}
				}
				
				String row;
				//int wordNumber = 0;
				ArrayList<String> words = new ArrayList<String>();
				
				//Read every row of the document(Starts on second line
				while((row = reader.readLine()) != null) {
					row = row.toLowerCase();
					//split row into an array based on spaced
					for(String word: row.split(" ")){
						//wprd already found
						if(map.containsKey(word)) {
							WordInfo info = map.get(word);
							info.value += 1;
						//not already found but in the value arraylist
						}else if(values.contains(word)){
							map.put(word, new WordInfo(word, word.length(), 1, wordNumber));
						}
						//wordNumber += 1;
					}
				}
				//write values that were found and not found to wights.txt
				for(String key : values) {
					WordInfo info = map.get(key);
					if(info==null) {
						writer.write(key + "," + key.length() + ",0\n");
					}else {
						writer.write(key + "," + info.weight + "," + info.value + "\n");
					}	
				}
				writer.close();
				reader.close();
	    	}catch (IOException e) {
				e.printStackTrace();
			}catch (IndexOutOfBoundsException e) {
				e.printStackTrace();
			}
		}
}