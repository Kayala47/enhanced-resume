import argparse
import typing
from numpy.testing._private.utils import assert_string_equal
import pandas as pd
import random
from typing import List
import os
import glob
import csv


def sample_k(k: int, csv_filename: str, new_filename: str):
    """[summary]

    Args:
        k (int): [description]
        csv_filename (str): [description]
        new_filename (str): [description]
    """
    f = open(csv_filename)
    reader = csv.reader(f)
    num_lines = len(list(reader)) - 1  # number of records in file (excludes header)

    skiprows = sorted(random.sample(range(1, num_lines + 1), num_lines - k))

    df = pd.read_csv(csv_filename, skiprows=skiprows)

    selected_list = df["Job Description"]

    # write all the listings to the file, adding a line break between each
    with open(new_filename, "w") as f:
        for listing in selected_list:
            listing = listing.replace("\n", "")
            f.write(listing)
            f.write("\n")


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

    for assignee in assignees:
        cwd = os.getcwd()
        print(cwd)
        new_filename = cwd + "/weekly_assignments/" + assignee + ".txt"

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

    cli.add_argument(
        "--filename",
        nargs=1,
        type=str,
        default="/Users/loan/Desktop/pai_resume/enhanced-resume/output_csvs/0.csv",
    )

    args = cli.parse_args()

    assign_tasks(args.filename[0], args.assignees, args.num)


if __name__ == "__main__":
    main()
