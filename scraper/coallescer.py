import os
import glob
import pandas as pd


def main():

    os.chdir("../output_csvs")  # change to directory with all the files
    extension = 'csv'

    # grabs all files with csv extension
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    print(all_filenames)

    # concatenates all files here
    combined_csv = pd.concat(
        [pd.read_csv(f) for f in all_filenames])

    combined_csv.to_csv("../final_output.csv")


if __name__ == "__main__":
    main()
