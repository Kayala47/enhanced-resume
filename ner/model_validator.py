import numpy as np
import pandas as pd
import spacy
import re
import trained_data
import random
import plac
from pathlib import Path
from tqdm import tqdm  # loading bar

# grab the directory where the model is stored
model_dir = "./spacy_model"
# nlp = spacy.load(model_dir)
try:
    nlp = spacy.load(model_dir)
except:
    nlp = spacy.blank('en')  # create blank Language class
    print("Created blank 'en' model")

n_iter = 100

# reads in the csv of tagged data
df = pd.read_csv("tagged_data.csv")
# text_list = df['Finished Text'] #grabs the processed data portion
# text_list = df['Pre-processing']
text_list = trained_data.TRAIN_DATA

# for i, stuff in enumerate(df['Finished Text']):
#     # print(type(stuff))
#     print(type(stuff))
#     print(f" The text is: {stuff}")
#     if (type(stuff) == float):
#         print(f"Index = {i}")
#         print(f" The text is: {stuff}")

test_perc = .3  # percentage of the list that's going to be used to train
train_num = int(len(text_list) * test_perc)

train_list = text_list.copy()
test_list = []

for i in range(0, train_num):

    # move the element from the train list to the test list
    index = random.randint(0, len(train_list) - 1)
    test_list.append(train_list[index])
    del train_list[index]


# create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)
# otherwise, get it so we can add labels
else:
    ner = nlp.get_pipe('ner')

# add labels
for _, annotations in train_list:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

    # get names of other pipes to disable them during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(train_list)
        losses = {}
        for text_num, annotations in tqdm(train_list):
            print([text_num])
            # print(annotations)
            nlp.update(
                [df['Finished Text'][text_num]],  # batch of texts
                [annotations],  # batch of annotations
                drop=0.5,  # dropout - make it harder to memorise data
                sgd=optimizer,  # callable to update weights
                losses=losses)
        print(losses)


# save model to output directory
if model_dir is not None:
    model_dir = Path(model_dir)
if not model_dir.exists():
    model_dir.mkdir()
nlp.to_disk(model_dir)
print("Saved model to ", model_dir)

total = 0
correct = 0

# test the saved model
print("Loading from", model_dir)
nlp2 = spacy.load(model_dir)
for num, annotations in test_list:
    doc = nlp2(df['Finished Text'][num])
    correct_list = annotations.get('entities')
    # print(doc.items)
    for i, ent in enumerate(doc.ents):
        try:
            (c_start, c_end, c_attr) = correct_list[i]

            if (ent.start_char == c_start and ent.end_char == c_end and ent.label_ == c_attr):
                correct += 1
                total += 1
            else:
                total += 1

        except:
            total += 1

    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

print(f"{correct} out of {total} entries")
print(f"Total accuracy = {int((correct/total) * 100)}%")
