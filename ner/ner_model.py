import numpy as np
import pandas as pd
import spacy
import re
import trained_data
import random
import plac
from pathlib import Path
from tqdm import tqdm  # loading bar

model = None
output_dir = "./output"
n_iter = 100

nlp = spacy.load("en_core_web_sm")

df = pandas.read_csv("tagged_data.csv")

x = df[0]['Finished Text']
print(x)


if model is not None:
    nlp1 = spacy.load(model)  # load existing spaCy model
    print("Loaded model '%s'" % model)
else:
    nlp1 = spacy.blank('en')  # create blank Language class
    print("Created blank 'en' model")

# create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
if 'ner' not in nlp1.pipe_names:
    ner = nlp1.create_pipe('ner')
    nlp1.add_pipe(ner, last=True)
# otherwise, get it so we can add labels
else:
    ner = nlp1.get_pipe('ner')

# add labels
for _, annotations in trained_data.TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

    # get names of other pipes to disable them during training
other_pipes = [pipe for pipe in nlp1.pipe_names if pipe != 'ner']
with nlp1.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp1.begin_training()
    for itn in range(n_iter):
        random.shuffle(trained_data.TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(trained_data.TRAIN_DATA):
            nlp1.update(
                [text],  # batch of texts
                [annotations],  # batch of annotations
                drop=0.5,  # dropout - make it harder to memorise data
                sgd=optimizer,  # callable to update weights
                losses=losses)
        print(losses)


# test the trained model
for text, _ in trained_data.TRAIN_DATA:
    doc = nlp1(x)
    print('Entities', [(ent.text, ent.label_) for ent in doc.ents])


# save model to output directory
if output_dir is not None:
    output_dir = Path(output_dir)
if not output_dir.exists():
    output_dir.mkdir()
nlp.to_disk(output_dir)
print("Saved model to", output_dir)


# test the saved model
print("Loading from", output_dir)
nlp2 = spacy.load(output_dir)
for text, _ in trained_data.TRAIN_DATA:
    doc = nlp2(text)
    print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

# nlp = spacy.load("en_core_web_sm")

# # import data
# df = pd.read_csv('../data_processing/processed_output_csvs/final_output.csv')

# for index, row in df.iterrows():
#     # print(list(df.columns))
#     print(row['Finished Text'])

#     doc = nlp(row['Finished Text'])

#     ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
#     print(ents)
