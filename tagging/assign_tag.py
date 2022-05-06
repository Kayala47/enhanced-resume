import argparse
import typing
from numpy.testing._private.utils import assert_string_equal
import pandas as pd
import random
import unicodedata
from typing import List
import os
import glob
import csv
import codecs
from pathlib import Path
from icecream import ic


def sample_k(k: int, csv_filename: str, new_filename: str):
    """[summary]

    Args:
        k (int): [description]
        csv_filename (str): [description]
        new_filename (str): [description]
    """

    print(f"{new_filename} = new filename")
    df = pd.read_csv(csv_filename, encoding="unicode_escape")
    num_lines = df.shape[0] - 1  # number of records in file (excludes header)

    skiprows = sorted(random.sample(range(1, num_lines + 1), num_lines - k))

    df = pd.read_csv(csv_filename, skiprows=skiprows, encoding="unicode_escape")

    # df = df["Job Description"]

    # write all the listings to the file, adding a line break between each
    with open(new_filename, "w+", encoding="unicode escape") as f:
        for i, row in df.iterrows():
            # print(row[3])
            content = str(row[2]).replace("\r\n", " ")
            # ic(content)
            # manually removes some unicode
            content = (
                content.replace("_x000D_", " ")
                .replace("\xe2\x80\x99", "'")
                .replace("\xe2\x80\x98", "'")
                .replace("\xe2\x80\x9c", '"')
                .replace("\xe2\x80\x9d", '"')
                .replace("\xe2\x80\x94", " - ")
                .replace("\xe2\x80\x93", " - ")
                .replace("\xe2\x80\x92", " - ")
                .replace("\xe2\x80\x91", " - ")
                .replace("\xe2\x80\x90", " - ")
            )
            # removes the rest of the unicode
            normalized = (
                unicodedata.normalize("NFKD", content)
                .encode("ascii", "ignore")
                .decode("ascii")
            )
            # ic(normalized)
            f.write(normalized)
            f.write(" \n ")


def assign_tasks(filename: str, assignees: List[str], num_assigned: int):
    """Given a csv file, a list of assignees, and a number to assign, creates
    text files for each assignee to tag.

    Args:
        filename (str): path to csv file
        assignees (List(str)): list of people to assign to
        num_assigned (int): number of listings to assign to each person
    """

    # strat: for each of the assignees, call the sample_k function with num_assigned as the arg
    assert len(assignees) > 0

    assert filename != ""

    weekly_assignments_path = Path(".\\weekly_assignments\\")

    for assignee in assignees:
        cwd = os.getcwd()
        print(cwd)

        new_filename = weekly_assignments_path.joinpath(f"{assignee}.txt")

        # if we're assigning a new file to someone, delete the old file
        try:
            os.remove(new_filename)
        except:
            print("failed to delete")
            pass  # if we couldn't delete it, no problem. prob doesn't exist

        sample_k(num_assigned, filename, new_filename)


def main():

    cli = argparse.ArgumentParser()

    # add argument to pass in a list of names
    cli.add_argument(
        "--assignees",
        nargs="*",  # with 0 or more, will create list
        type=str,  # will be list of names
        default=[],  # if nothing passed in, no assignees
    )

    cli.add_argument(
        "--num",
        nargs=1,
        type=int,
        default=50,
    )

    default_path = Path("../data_processing/processed_output_csvs/processed_final.csv")

    cli.add_argument(
        "--filename",
        nargs=1,
        type=str,
        default=default_path,
    )

    args = cli.parse_args()

    assign_tasks(args.filename, args.assignees, args.num)


if __name__ == "__main__":
    main()
