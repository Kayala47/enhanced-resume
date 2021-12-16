import numpy as np
import pandas as pd
import spacy
import re
import random
import plac
from pathlib import Path
from tqdm import tqdm  # loading bar
import json
from icecream import ic # really good debugger
import os

def validate_model(model_dir: str, test_data: str) -> float:

    # load in training data
    with open(test_data, 'r') as test_file:
        tagged_data = json.load(test_file)
        annotations = tagged_data['annotations']

    # test the saved model
    print("Loading from", model_dir)

    model = spacy.load(model_dir)

    correct = 0
    total = 0

    for text, ent_dict in annotations:
        doc = model(text)

        
        if not len(doc.ents) > 0 :
            # nothing to compare anyway
            continue

        total += ic(len(doc.ents))
        
        # print(doc.items)
        for i, ent in enumerate(doc.ents):
            try:
                (c_start, c_end, c_attr) = ent_dict['entities'][i]

                if (ent.start_char == c_start and ent.end_char == c_end and ent.label_ == c_attr):
                    correct += 1
                    
            except Exception as e:
                ic(e)
                pass

        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

    print(f"{correct} out of {total} entries")
    print(f"Total accuracy = {int((correct/total) * 100)}%")


os.chdir('/Users/loan/Desktop/pai_resume/enhanced-resume/ner/')
ic(validate_model('./output/', 'hand_tagged.json'))

