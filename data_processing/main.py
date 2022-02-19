import csv
import sys
import stopword_remover
import tokenizer
import os

# TODO: Consider making all text lowercase, I noticed a capitalized 'The'
#      was able to slip past the stop word filter, for example.

"""
remove_stopwords
takes in a csv file name from the output csv folder

returns a duplicate of the inputted csv file, but with
new columns to hold: 
1) tokenized data 
2) tokenized data with stop words removed
"""


def remove_stopwords(csv_name):

    print(os.getcwd())

    with open(csv_name, "r", encoding="utf-8") as read_obj, open(
        "./processed_output_csvs/processed_final", "w", encoding="utf-8", newline=""
    ) as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = csv.reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = csv.writer(write_obj)
        # Add title row to new csv
        row0 = next(csv_reader)
        row0.append("Tokenized")
        row0.append("Stop Words Removed")
        row0.append("Finished Text")
        csv_writer.writerow(row0)
        # Read each row of the input csv file as list
        for row in csv_reader:

            # description is in column 2
            description_text = row[2].lower()

            # tokenization here...
            tokenized_data = tokenizer.tokenize(description_text)
            row.append(tokenized_data)

            # stop word removal here...
            stopwords_removed = stopword_remover.remove_from(tokenized_data)
            row.append(stopwords_removed)

            finished = " ".join(stopwords_removed)
            row.append(finished)

            # Add the updated row / list to the output file
            csv_writer.writerow(row)


def main(csv_name):
    remove_stopwords(csv_name)
    print("generated the new csv")


if __name__ == "__main__":
    # remove_stopwords(sys.argv[1])
    remove_stopwords("../output_from_scraper/final_output.csv")
    print("generated the new csv")
