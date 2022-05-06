from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager

import time
import sys
import pandas as pd

from threading import Thread

import requests
from bs4 import BeautifulSoup

THREADS = 30 # MUST BE FACTOR OF LISTINGS PER PAGE (30)

def scrape_single(query):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    kw_param = "%20".join(query.split(" "))
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={kw_param}"

    driver.get(url)  # open jobs page
    
    listing = (
        WebDriverWait(driver, 10)
        .until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "react-job-listing",
                )
            )
        )
    )

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

    return desc
    # return {
    #     "Company Name": name,
    #     "Job Title": title,
    #     "Job Location": loc,
    #     "Job Description": desc,
    # }

def thread_scrape(listings, scraped):
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

def scrape_page(job_listings):
    scraped_listings = []
    threads = []
    tsz = int(len(job_listings)/THREADS)

    for n in range(0,THREADS):
        t = Thread(target=thread_scrape, args=(job_listings[n*tsz:(n+1)*tsz], scraped_listings))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
        
    return scraped_listings

def scrape(query, num_pages):
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("start-maximized")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    kw_param = "%20".join(query.split(" "))
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={kw_param}"

    driver.get(url)  # open jobs page
    scraped = []

    for _ in range(0,num_pages):
        (
            WebDriverWait(driver, 10)
            .until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        "react-job-listing",
                    )
                )
            )
        )

        job_listings = driver.find_elements_by_class_name("react-job-listing")

        scraped += scrape_page(job_listings)

        try:
            driver.find_element_by_class_name("nextButton").click()
        except ElementClickInterceptedException:
            elem = driver.find_element_by_class_name("modal_closeIcon-svg")
            ac = ActionChains(driver)
            ac.move_to_element(elem).click().perform()  # move cursor to X SVG and click
            time.sleep(2)
            driver.find_element_by_class_name("nextButton").click()

    return pd.DataFrame(scraped)

def write_to_csv(df, path):
    pd.set_option("display.max_colwidth", None)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(sys.argv)
        print(
            "Incorrect number of arguments, should be 'python glassdoor_scraper.py <search_query> <num_pages>'"
        )
    else:
        try:
            query = str(sys.argv[1])
            num_pages = int(sys.argv[2])
        except:
            print(
                "Incorrect argument format, should be 'python glassdoor_scraper.py <search_query> <num_pages>'"
            )
        scraped = scrape('machine learning', num_pages)
        write_to_csv(scraped, './output.csv')