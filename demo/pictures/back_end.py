
'''
Purpose: takes in a string detailing the type of job a user is looking for, opens up a 
web browser to grab some jobs, and passes that back to the calling function (which will be
the front end)
'''


import sys
import pandas as pd

sys.path.append('../scraper')
from glassdoor_scraper import get_jobs
# adds this folder to path so I can grab the scraper py files



url = 'https://www.glassdoor.com/Job/jobs.htm?context=Jobs&suggestCount=0&suggestChosen=false&clickSource=searchBox&typedKeyword=Software%20Engineer&sc.keyword=Software%20Engineer'


def scrape5(job: str):

    df = get_jobs(5, url)
    df.drop('Job Title')
    print(df)


if __name__ == "__main__":
    scrape5(url)
    print("gathered data")
