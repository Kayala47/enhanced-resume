import numpy as np
from numpy.core.fromnumeric import size
import pandas as pd
import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example
from icecream import ic

import re
import random
import plac
from pathlib import Path
from tqdm import tqdm  # loading bar
import json
import os


def train_model(output_dir: str, training_data: str, testing_data: str):

    # start with blank model
    model = None
    output_dir = "./spacy_model"
    n_iter = 100

    train_perc: float = 0.8  # percent of tagged data used for training

    # load in tagged data
    with open(training_data, "r") as train_file:
        tagged_data = json.load(train_file)
        annotations = tagged_data["annotations"]

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner", last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for label in tagged_data["classes"]:
        ner.add_label(label)

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER

        optimizer = nlp.begin_training()
        for itn in range(n_iter):

            random.shuffle(annotations)
            losses = {}
            ic(annotations)

            # using minibatch to combine the examples
            # batches = minibatch(annotations, size=2)
            # ic(batches)

            for text, entities in tqdm(annotations):

                example_list = []

                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, entities)
                example_list.append(example)

                nlp.update(
                    example_list,  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses,
                )
                print(losses)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

    with open(testing_data, "r") as test_file:
        tagged_data = json.load(test_file)
        test_annotations = tagged_data["annotations"]

    # test the saved model
    print("Loading from", output_dir)
    saved_model = spacy.load(output_dir)

    for text, ent_dict in test_annotations:

        comparison_ent = ent_dict["entities"]

        doc = saved_model(text)
        print(
            f"Entities recognized by the model: \n {[(ent.text, ent.label_) for ent in doc.ents]}"
        )
        print(
            f"Entities tagged by hand:  \n {[(text[start:end], tag) for start, end, tag in comparison_ent]}"
        )


# os.chdir("/Users/loan/Desktop/pai_resume/enhanced-resume/ner/")

train_model("./spacy_model", "hand_tagged.json", "hand_tagged.json")
