import glob
import os
from os import walk
from typing import List
import json

os.chdir("./tagging")
# Get all files under hand_tagged
file_names: List[str] = glob.glob("./hand_tagged/*")
print(file_names)

# start a new dictionary and add all the files in
def merge_JsonFiles(to_merge: List[str], output_file: str):
    result = dict()
    for f1 in to_merge:
        with open(f1, "r") as infile:
            result = result | (
                json.load(infile)
            )  #'OR' is the pythonic way to combine dictionaries

    # write to output file in scraper directory
    with open(output_file, "w") as output_file:
        json.dump(result, output_file)


merge_JsonFiles(file_names, "../ner/hand_tagged.json")

