"""
Purpose: takes in a string detailing the type of job a user is looking for, opens up a 
web browser to grab some jobs, and passes that back to the calling function (which will be
the front end)
"""

# STOP - IMPORTANT
# Only save without formatting - if you're on VSCode, find that by hitting Ctrl+Shift+P> "Save without formatting"

import sys

sys.path.append("../scraper")
# adds this folder to path so I can grab the scraper py files
from glassdoor_new import (
    scrape,
    scrape_one,
)  # IMPORTANT - this must go after sys.path.append('../scraper')


def scrape_amount(job: str, amount: int):
    df = scrape(job, amount)
    return df


def scrape_single(title: str, company: str):
    desc = scrape_one(f"{title} {company}")
    return desc
