
'''
Purpose: takes in a string detailing the type of job a user is looking for, opens up a 
web browser to grab some jobs, and passes that back to the calling function (which will be
the front end)
'''

#STOP - IMPORTANT
# Only save without formatting - if you're on VSCode, find that by hitting Ctrl+Shift+P> "Save without formatting"

import sys

sys.path.append('../scraper')
# adds this folder to path so I can grab the scraper py files
from glassdoor_scraper import get_jobs, get_onelisting #IMPORTANT - this must go after sys.path.append('../scraper')


def scrape_amount(job: str, amount: int):
    df = get_jobs(job, amount)
    return df

def scrape_single(title: str, company: str):
    df = get_onelisting((title, company))
    return df


