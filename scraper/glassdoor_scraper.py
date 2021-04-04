# selenium is our scraper, requires a webdriver for each browser you use
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

import time  # to allow waiting for load
import pandas as pd  # keep a database of our job listings


def get_jobs(num_jobs: int, url: str):
    '''
    Opens a chrome browser that manually clicks on job postings and scrapes the description

    Inputs:
    Keyword = the search term for the job listings you want. Ie, "data scientist"
    num_jobs = number of listings you want to scrape. Low default is for testing. 
    '''
    print("begain scraping")
    # we need a webdriver installed every time. However, we can get it to install
    # automatically instead of manually
    options = webdriver.ChromeOptions()

    # Uncomment the lines below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')
    options.add_argument('start-maximized')

    # the driver is responsible for opening the new window
    # installs driver each time
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # for now, hardcoded. Later, will depend on keyword entered above
    # TODO: change to allow different keywords
    url = url

    driver.get(url)  # open webpage

    jobs_list = []  # list of already-scraped listings

    while len(jobs_list) < num_jobs:
        # we need a certain amt (num_jobs). If we haven't gotten that amount, keep scraping

        # Let the page load. Right now, hardcoded this way.
        # TODO: set to wait until page loads
        time.sleep(2)

        '''
        Lot's of these websites have annoying pop-ups asking you to sign up for an 
        account. They only come up when you try to click something. To get rid of 
        them, we "bait" the website by trying to click somewhere, and then find the
        "x" to close that pop-up.
        '''

        try:
            driver.find_element_by_class_name(
                "react-job-listing").click()
        except ElementClickInterceptedException:
            # something got in the way of our click
            pass  # this is just bait anyway, so hopefully we've spawned the popup
        except NoSuchElementException:
            print("couldn't click anywhere")
            pass

        # now we wait for the pop-up to load
        time.sleep(5)

        # and then try to click the x to close it
        try:
            elem = driver.find_element_by_class_name("modal_closeIcon-svg")
            print(elem)  # just to make sure we've found it

            '''
            The x is disguised as an svg, so it's not a clickable element.
            What we do instead is find its location and move our cursor there to 
            click it manually.
            '''
            ac = ActionChains(driver)
            ac.move_to_element(elem).click().perform()
        except NoSuchElementException:
            # there is no x to close - serious issue!
            print("couldn't click pop-up")
            pass

        # for glassdoor, each job listing has the "react-job-listing" class
        # you'll need to find the class name for your specific site
        job_listings = driver.find_elements_by_class_name("react-job-listing")

        for job_listing in job_listings:
            # go through each listing on the site

            # helps track progress through terminal
            print("Progress: {}".format(
                "" + str(len(jobs_list)) + "/" + str(num_jobs)))

            # we only want to scrape a certain amount - don't overwhelm users
            if len(jobs_list) >= num_jobs:
                break

            job_listing.click()  # Go to this listing, and get react to load it

            # wait for it to load
            time.sleep(1)

            # bool to check if we've gotten info we need from a listing
            collected_successfully = False

            while not collected_successfully:
                try:

                    # again, need to find specific class name for each of these for your website

                    # find company name
                    # company_name = driver.find_element_by_xpath(
                    #     './/div[@class="employerName"]').text

                    company_name = -1

                    # job_title = driver.find_element_by_xpath(
                    #     './/div[contains(@class, "title")]').text
                    job_title = -1

                    # find job description
                    job_description = driver.find_element_by_xpath(
                        './/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    # if you can't get the info, it probably hasn't loaded. wait a bit
                    print("couldn't find those")
                    time.sleep(1)

            # adds the listing to our jobs list
            jobs_list.append({
                "Job Title": job_title,
                "Company Name": company_name,
                "Job Description": job_description
            })

        # Clicking on the "next page" button
        # you'll do this once you run out of listings on one page
        try:
            # driver.find_element_by_xpath(
            #     './/li[@class="pagination-next"]//a').click()

            '''
                The next page button is also an svg, not a button. We need to move our
                cursor to where the svg is and click that.

            '''
            elem = driver.find_element_by_css_selector(
                '[data-test="pagination-next"]')
            print(elem)  # just to make sure we've found it

            ac = ActionChains(driver)
            ac.move_to_element(elem).click().perform()
        except NoSuchElementException:
            # not enough job listings to satisfy criteria
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(
                num_jobs, len(jobs_list)))
            break

    return pd.DataFrame(jobs_list)


def gather_data(filename: str = "./output.csv", num_jobs: int = 5, url: str = "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=machine%20learning%20engineer%20jobs"):
    '''
    Performs scraping operation and creates a text file with our data

    Inputs:
    filename = path to file you want data in. By default, creates a file in same dir
    '''

    # by default, will scrape 5 listings
    df = get_jobs(num_jobs, url)

    pd.set_option('display.max_colwidth', None)

    # open a file in write mode
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    gather_data()
    print("gathered data")
