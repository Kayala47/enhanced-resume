import sys  # for command-line args

from numpy import loadtxt  # loads txt file into array


import threading  # for multithreading

from glassdoor_scraper import gather_data

import os
import glob
import pandas as pd

NUM_DESCR = 100  # how many descriptions we want to scrape from each job
CSV_BASE = "../outputcsvs"


class scraperThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        print(f"Created Thread {self.threadID} and began scraping {self.name}")

        self.filename = r'../output_csvs/' + str(threadID) + ".csv"

    def run(self):
        gather_data(self.filename, NUM_DESCR, self.name)


class mainThread(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    def run(self):
        multi_threaded_scrape(self.filename)


def multi_threaded_scrape(filename: str = "urls.txt"):
    '''
    Takes a text file containing urls and starts a glassdoor_scraper instance for each of them.

    Multi-threaded.


    '''
    # print("got to main")
    urls = loadtxt(filename, dtype=str, comments="#",
                   delimiter="\n", unpack=False)

    num_threads = len(urls)

    threads_list = []

    for i, val in enumerate(urls):
        # print(val)
        new_thread = scraperThread(i, val)
        threads_list.append(new_thread)
        new_thread.start()


def main():
    master = mainThread("urls.txt")
    master.start()
    master.join()
    # multi_threaded_scrape()  # do all the scraping first

    os.chdir("../output_csvs")  # change to directory with all the files
    extension = 'csv'

    # grabs all files with csv extension
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    # concatenates all files here
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

    combined_csv.to_csv("final_output.csv")


if __name__ == "__main__":
    multi_threaded_scrape()
