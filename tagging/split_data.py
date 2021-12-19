import glob
import os
from os import walk
from typing import List
import json
import random


def main(
    mergefile_path: str, test_out_path: str, train_out_path: str, test_perc: float
):

    with open(mergefile_path, "r") as merge_file:
        mf = json.load(merge_file)

        # make a new dictionary
        # classes stays the same
        # annotations keeps only test_perc amount

        classes = mf["classes"]
        annotations = mf["annotations"]

        random.shuffle(annotations)
        test_idx = int((len(annotations) * test_perc) - 1)
        test_annot = annotations[:test_idx]

        train_annot = annotations[test_idx:]

        train_dict = {"classes": classes, "annotations": train_annot}
        test_dict = {"classes": classes, "annotations": test_annot}

    with open(test_out_path, "w") as test_out:
        json.dump(test_dict, test_out)

    with open(train_out_path, "w") as train_out:
        json.dump(train_dict, train_out)


main("../ner/hand_tagged.json", "../ner/test_data.json", "../ner/train_data.json", 0.4)
