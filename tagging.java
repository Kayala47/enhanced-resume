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
	  
	  public WordInfo(String word, int value, int weight, int importance) { 
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
				int wordNumber = 0;
				ArrayList<String> words = new ArrayList<String>();
				
				while((row = reader.readLine()) != null) {
					row = row.toLowerCase();
					for(String word: row.split(" ")){
						if(map.containsKey(word)) {
							WordInfo info = map.get(word);
							info.value += 1;
							
						}else if(values.contains(word)){
							map.put(word, new WordInfo(word, 1, word.length(), wordNumber));
							words.add(word);
						}
						wordNumber += 1;
					}
				}
				for(String key : words) {
					WordInfo info = map.get(key);
					writer.write(key + "," + info.value + "," + info.weight + "\n");
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