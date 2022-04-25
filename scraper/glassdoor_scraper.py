import re
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import sys  # for CLI arguments
import time  # to allow waiting for load
import pandas as pd  # keep a database of our job listings
from tqdm import tqdm  # progress bar

import requests
from bs4 import BeautifulSoup

# read credentials from .env to avoid public repo exposure
import os


# opens a chrome browser and scrapes jobs description for a given search

# INPUTS: query = the search term for the job listings | num_jobs = number of listings scrape
def get_jobs(query: str, num_jobs: int):
    """
    Opens a chrome browser that manually clicks on job postings and scrapes the description

    Inputs:
    Keyword = the search term for the job listings you want. Ie, "data scientist"
    num_jobs = number of listings you want to scrape. Low default is for testing.
    """
    print("Began scraping")

    ## CONFIGURE THE WEBDRIVER ##
    # we need a webdriver installed every time. However, we can get it to install
    # automatically instead of manually

    # automatically install a webdriver

    options = webdriver.ChromeOptions()

    # uncomment below to activate headless
    # options.add_argument("headless")
    # options.add_argument("start-maximized")

    # installs driver each time
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    print("\n\n")
    print(f"Scraping {num_jobs} Job Listings for '{query}'")

    ## SIGN IN FLOW ##
    try:
        login_ac = ActionChains(driver)

        # go to home page first to emulate real user
        driver.get("https://www.glassdoor.com/index.htm")

        # click sign in buttoon
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="SiteNav"]/nav/div[2]/div/div/div/button')
            )
        ).click()
        time.sleep(0.5)

        # build ActionChain
        email_elem = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "userEmail"))
        )
        login_ac.move_to_element(
            email_elem
        ).click()  # password field isn't an input, so have to use clicks to fill form
        login_ac.pause(1)
        login_ac.send_keys(os.getenv("GLASSDOOR_EMAIL"))
        login_ac.pause(1)
        login_ac.send_keys(Keys.TAB)
        login_ac.pause(1)
        login_ac.send_keys(os.getenv("GLASSDOOR_PASSWORD"))
        login_ac.pause(1)
        login_ac.send_keys(Keys.ENTER)

        # perform ActionChain
        login_ac.perform()
        time.sleep(3)
    except:
        print("[ERR] Failed to login, will try as guest")

    # construct a url from keywords
    kw_param = "%20".join(query.split(" "))
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={kw_param}"

    driver.get(url)  # open jobs page

    ## DEAL WITH THE POPUP ##

    time.sleep(2)

    # bait the pop-up by clicking on a job listing
    try:
        driver.find_element_by_class_name("react-job-listing").click()
    except (ElementClickInterceptedException, NoSuchElementException):
        pass

    time.sleep(1)

    # close the popup
    try:
        elem = driver.find_element_by_class_name("modal_closeIcon-svg")
        ac = ActionChains(driver)
        # move cursor to X SVG and click
        ac.move_to_element(elem).click().perform()
    except NoSuchElementException:
        # there is no x to close - serious issue!
        print("[ERR] Failed to close popup")
        pass

    jobs_list = []  # list of already-scraped listings

    pbar = tqdm(total=num_jobs)  # initialize progress bar

    ## SCRAPE 1 PAGE OF LISTINGS AT A TIME ##
    while len(jobs_list) < num_jobs:
        # we need a certain amt (num_jobs). If we haven't gotten that amount, keep scraping

        time.sleep(2)

        # enumerate job listings
        job_listings = driver.find_elements_by_class_name("react-job-listing")

        # go through each listing on the site
        for job_listing in job_listings:
            stale_page = False

            # we only want to scrape a certain amount - don't overwhelm users
            if len(jobs_list) >= num_jobs:
                break

            try:
                job_listing.click()  # go to this listing, and get react to load it
            except:
                print("[ERR] Stale element, skipping")
                stale_page = True  # if the page is stale, we need to go to the next page
                pass

            # scrape the listing
            if not stale_page:
                try:
                    # TODO: find company and title
                    job_info = job_listing.text.split("\n")

                    # check to see if there is a rating, then remove it
                    try:
                        float(job_info[0])
                        job_info.pop(0)
                    except ValueError:
                        pass

                    job_company = job_info[0]
                    job_title = job_info[1]
                    job_location = job_info[2]

                    # find job description
                    job_description = (
                        WebDriverWait(driver, 5)
                        .until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    './/div[@class="jobDescriptionContent desc"]',
                                )
                            )
                        )
                        .get_attribute('innerText')
                    )

                    time.sleep(0.25)

                    # adds the listing to our jobs list
                    jobs_list.append(
                        {
                            "Company Name": job_company,
                            "Job Title": job_title,
                            "Job Location": job_location,
                            "Job Description": job_description,
                        }
                    )

                    pbar.update(1)
                except:
                    # if you can't get the info, skip this listing
                    pass

        # advance to the next page of job listings
        try:
            driver.find_element_by_class_name("nextButton").click()
        except NoSuchElementException:
            # not enough job listings to satisfy criteria
            print(
                f"[ERR] Terminated before target. Scraped {len(jobs_list)}/{num_jobs}"
            )
            break

    pbar.close()

    return pd.DataFrame(jobs_list)


# Run the scraper and output to a csv file
# Input: (filename to write to, job keywords, number of jobs to scrape)
def gather_data(
    filename: str = "./output.csv",
    keywords: str = "machine learning",
    num_jobs: int = 5,
):

    df = get_jobs(keywords, num_jobs)  # scrape the job listing

    pd.set_option("display.max_colwidth", None)
    df.to_csv(filename, index=False)  # write to an output csv


def get_onelisting(url):
    r = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    })

    soup = BeautifulSoup(r.text, 'html.parser')

    desc = soup.find('div', {'id': 'JobDescriptionContainer'}).text
    job_info = list(soup.find('div', {'class': 'smarterBannerEmpInfo'}).stripped_strings)

    return pd.DataFrame([
        {
            "Company Name": job_info[0],
            "Job Title": job_info[1],
            "Job Location": job_info[2],
            "Job Description": desc,
        }
    ])


# Pass arguments through the command line: 'python scraper/glassdoor_scraper.py <num_jobs> <search_query>
if __name__ == "__main__":
    try:
        num = int(sys.argv[1])
        query = str(sys.argv[2])
    except:
        print("Incorrect format, use: 'python glassdoor_scraper.py <num_jobs> <search_query>'")

    gather_data(keywords=query, num_jobs=num)
    print("Finished Scraping")
