
'''
Purpose: takes in a string detailing the type of job a user is looking for, opens up a 
web browser to grab some jobs, and passes that back to the calling function (which will be
the front end)
'''

#STOP - IMPORTANT
# Only save without formatting - if you're on VSCode, find that by hitting Ctrl+Shift+P> "Save without formatting"

import sys
import pandas as pd

sys.path.append('../scraper')
# adds this folder to path so I can grab the scraper py files
from glassdoor_scraper import get_jobs #IMPORTANT - this must go after sys.path.append('../scraper')


url = 'https://www.glassdoor.com/Job/jobs.htm?context=Jobs&suggestCount=0&suggestChosen=false&clickSource=searchBox&typedKeyword=Software%20Engineer&sc.keyword=Software%20Engineer'


def scrape_amount(job: str, amount: int):

    df = get_jobs(amount, url)
    # df.drop('Job Title')
    return df
    # print(df)


if __name__ == "__main__":
    data = scrape5(url)
    print(data)
    print("gathered data")
