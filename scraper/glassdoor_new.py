from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import json
import pandas as pd

from threading import Thread

import requests
from bs4 import BeautifulSoup

THREADS = 30 # MUST BE FACTOR OF LISTINGS PER PAGE (30)

def scrape_single(listings, scraped):
    for listing in listings:
        a_tag = listing.find_elements_by_tag_name('a')[1]
        url = a_tag.get_attribute('href')

        name = a_tag.text
        title = listing.get_attribute('data-normalize-job-title')
        loc = listing.get_attribute('data-job-loc')

        r = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
        })

        soup = BeautifulSoup(r.text, 'html.parser')
        desc = soup.find('div', {'id': 'JobDescriptionContainer'}).text

        scraped.append({
            "Company Name": name,
            "Job Title": title,
            "Job Location": loc,
            "Job Description": desc,
        })

def scrape_page(query):
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("start-maximized")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    kw_param = "%20".join(query.split(" "))
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={kw_param}"

    driver.get(url)  # open jobs page

    job_listings = driver.find_elements_by_class_name("react-job-listing")

    scraped_listings = []
    threads = []
    tsz = int(len(job_listings)/THREADS)

    for n in range(0,THREADS):
        t = Thread(target=scrape_single, args=(job_listings[n*tsz:(n+1)*tsz], scraped_listings))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
        
    return scraped_listings

if __name__ == "__main__":
    listings = scrape_page('machine learning')
    with open('test.json', 'w') as f:
        json.dump(listings, f)
