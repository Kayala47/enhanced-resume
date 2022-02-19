import os
import glob
import pandas as pd
import sys


def main(folder_name):

    # change to directory with all the files
    os.chdir(folder_name)
    extension = "csv"

    # grabs all files with csv extension
    all_filenames = [i for i in glob.glob("*.{}".format(extension))]
    print(all_filenames)

    # concatenates all files here
    combined_csv = pd.concat([pd.read_csv(f, delimiter=",") for f in all_filenames])

    combined_csv.to_csv("final_output.csv")


if __name__ == "__main__":
    print(sys.argv[1])
    main(sys.argv[1])
