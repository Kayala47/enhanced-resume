from re import search
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import sys  # for CLI arguments
import time  # to allow waiting for load
import pandas as pd  # keep a database of our job listings
from tqdm import tqdm  # progress bar

# read credentials from .env to avoid public repo exposure
import os
from dotenv import load_dotenv

load_dotenv()

# opens a chrome browser and scrapes jobs description for a given search
# INPUTS: query = the search term for the job listings | num_jobs = number of listings scrape
def get_jobs(query: str, num_jobs: int):
    # automatically install a webdriver
    options = webdriver.ChromeOptions()

    # uncomment below to activate headless
    # options.add_argument('headless')
    options.add_argument("start-maximized")

    # the driver is responsible for opening the new window
    # installs driver each time
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # sign in flow
    try:
        login_ac = ActionChains(driver)

        # go to home page first to emulate real user
        driver.get("https://www.glassdoor.com/index.htm")
        time.sleep(3)

        # click sign in buttoon
        driver.find_element_by_xpath(
            '//*[@id="SiteNav"]/nav/div[2]/div/div/div/button'
        ).click()  # TODO: un-hardcode this, should look for class name
        time.sleep(2)

        # build ActionChain
        # email_elem = driver.find_element_by_id("userEmail")
        email_elem = driver.find_element_by_class_name("css-1iw6ixi")
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

    jobs_list = []  # list of already-scraped listings

    pbar = tqdm(total=num_jobs)  # initialize progress bar

    while len(jobs_list) < num_jobs:
        # we need a certain amt (num_jobs). If we haven't gotten that amount, keep scraping

        # Let the page load. Right now, hardcoded this way.
        # TODO: set to wait until page loads
        time.sleep(2)

        # bait the pop-up by clicking on a job listing
        try:
            driver.find_element_by_class_name("react-job-listing").click()
        except (ElementClickInterceptedException, NoSuchElementException):
            pass

        time.sleep(3)  # wait for pop-up to load

        # close the popup
        try:
            elem = driver.find_element_by_class_name(
                "modal_closeIcon-svg"
            )  # x is not directly clickable
            ac = ActionChains(driver)
            ac.move_to_element(elem).click().perform()  # move cursor to X SVG and click
        except NoSuchElementException:
            # there is no x to close - serious issue!
            print("[ERR] Failed to close popup")
            pass

        # enumerate job listings
        job_listings = driver.find_elements_by_class_name("react-job-listing")

        # go through each listing on the site
        for job_listing in job_listings:
            # we only want to scrape a certain amount - don't overwhelm users
            if len(jobs_list) >= num_jobs:
                break

            job_listing.click()  # go to this listing, and get react to load it
            time.sleep(1)  # wait for it to load

            collected_successfully = (
                False  # keep this false until we successfully scrape the listing
            )

            # scrape the listing
            while not collected_successfully:
                try:
                    # TODO: find company and title
                    company_name = (
                        -1
                    )  # driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    job_title = (
                        -1
                    )  # driver.find_element_by_xpath('.//div[contains(@class, "title")]').text

                    # find job description
                    job_description = driver.find_element_by_xpath(
                        './/div[@class="jobDescriptionContent desc"]'
                    ).text
                    collected_successfully = True
                except:
                    # if you can't get the info, it probably hasn't loaded. wait a bit
                    print("[ERR] Couldn't fetch job info, trying again")
                    time.sleep(1)

            # adds the listing to our jobs list
            jobs_list.append(
                {
                    "Job Title": job_title,
                    "Company Name": company_name,
                    "Job Description": job_description,
                }
            )

            pbar.update(1)

        # advance to the next page of job listings
        try:
            # next page button is also an SVG, not a button
            elem = driver.find_element_by_css_selector('[data-test="pagination-next"]')

            ac = ActionChains(driver)
            ac.move_to_element(elem).click().perform()  # move to SVG and click
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
    print(f"Scraping {num_jobs} Job Listings for '{keywords}'")
    df = get_jobs(keywords, num_jobs)  # scrape the job listing
    pd.set_option("display.max_colwidth", None)
    df.to_csv(filename, index=False)  # write to an output csv


# Pass arguments through the command line: 'python scraper/glassdoor_scraper.py <num_jobs> <search_query>
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(sys.argv)
        print(
            "Incorrect number of arguments, should be 'python glassdoor_scraper.py <num_jobs> <search_query>'"
        )
    else:
        try:
            num = int(sys.argv[1])
            query = str(sys.argv[2])
        except:
            print(
                "Incorrect argument format, should be 'python glassdoor_scraper.py <num_jobs> <search_query>'"
            )
        gather_data(keywords=query, num_jobs=num)
        print("Finished Scraping")
