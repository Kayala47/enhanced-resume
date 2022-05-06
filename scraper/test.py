import requests
from bs4 import BeautifulSoup
import json
import time

job_list = []

HEADERS = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }

def get_list():
    r = requests.get('https://www.glassdoor.com/Job/machine-learning-jobs-SRCH_KO0,16.htm', headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    job_script_tag = soup.find('div', {'id': 'JobSearch'}).find('script', {'type': 'application/ld+json'})
    job_list = json.loads(job_script_tag.contents[0].string)
    job_links = [d['url'] for d in job_list['itemListElement']]

    return job_links

def scrape_job(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    desc = soup.find('div', {'id': 'JobDescriptionContainer'}).text

    job_info = list(soup.find('div', {'class': 'smarterBannerEmpInfo'}).stripped_strings)

    job_list.append(
        {
            "Company Name": job_info[0],
            "Job Title": job_info[1],
            "Job Location": job_info[2],
            "Job Description": desc,
        }
    )

    with open('test.json', 'w') as f:
        json.dump(job_list, f)

# jl = get_list()
scrape_job('https://www.glassdoor.com/partner/jobListing.htm?pos=101&ao=1110586&s=58&guid=0000018076e435e09df8e3e687f0b72c&src=GD_JOB_AD&t=SR&vt=w&cs=1_53c6b2dc&cb=1651262110275&jobListingId=1007828802844&cpc=D99DB9A39DE67464&jrtk=3-0-1g1re8do7q6ci801-1g1re8dorjoq9800-370a89299b54e9d8--6NYlbfkN0AFTl_suYmCFpmezcP_x2pMIeRyV7kapGxqRaQST_8rEnV59Rntjk4peviZZEfsodpC5OoahbVcOjUfTGBBgFWdP7wHVW1fFWWn6Se5saOZ-zq7i2qsDC7XwBkHNnf7ubf_ANa86DGkI8LAU01MheNchaB15syKQPTq2FbhKnLBwcZcnZXJQGZnBFKiM5D2KqlCWXGtEEvPGlozNt8iym-R32qZ7FUprMowfXD1XiyTBQV5eDe07vULMalNHhDINcuft0KKyUPh57wMFTZIsGH7WUIoo6g5h9uWyCtwDUlE-4PZzQOYH8UwaTVEh86LDNSgIzyrWy1CJ3sIfedHTTcNQccQYu9kgy2nXn7ett1VjwJthjqoEZFThX_5RN9lqw22wGxfikMIM0-dVfqNTNXeR0BI1TEET1gTIBWFv0EPPbqWG5ifEdwXeOPUqrrjcQL68zklofIMxlKqhPW0ofAB')

# payload = {
#   "operationName": "JobSearchQuery",
#   "variables": {
#     "searchParams": {
#       "keyword": "machine learning",
#       "numPerPage": 30,
#       "searchType": "SR",
#       "pageNumber": 2,
#       "pageCursor": "AB4AAYEAHgAAAAAAAAAAAAAAAdIKiaIAVwEBAQwOLqcD5hy6oNmoEH1NBsWNq4h9GME/Ejzg0x5vr7Toza+Hr5F5XlfLpF6VvD0MkVpl8NkZP8pJ2k9uJSx9ZkAuxwQKPkP8JE+QF9tjcqEo+569JgAA",
#       "filterParams": [
#         {
#           "filterKey": "includeNoSalaryJobs",
#           "values": "true"
#         },
#         {
#           "filterKey": "sc.keyword",
#           "values": "machine learning"
#         },
#         {
#           "filterKey": "locT",
#           "values": ""
#         },
#         {
#           "filterKey": "locId",
#           "values": ""
#         }
#       ],
#       "seoUrl": "false"
#     }
#   },
#   "query": "query JobSearchQuery($searchParams: SearchParams) {\n  jobListings(contextHolder: {searchParams: $searchParams}) {\n    ...SearchFragment\n    __typename\n  }\n}\n\nfragment SearchFragment on JobListingSearchResults {\n  adOrderJobLinkImpressionTracking\n  totalJobsCount\n  filterOptions\n  companiesLink\n  searchQueryGuid\n  indeedCtk\n  jobSearchTrackingKey\n  paginationCursors {\n    pageNumber\n    cursor\n    __typename\n  }\n  searchResultsMetadata {\n    cityPages {\n      cityBlurb\n      cityPagesStats {\n        bestCitiesForJobsRank\n        meanBaseSalary\n        population\n        unemploymentRate\n        __typename\n      }\n      displayName\n      employmentResources {\n        addressLine1\n        addressLine2\n        cityName\n        name\n        phoneNumber\n        state\n        zipCode\n        __typename\n      }\n      heroImage\n      isLandingExperience\n      locationId\n      numJobOpenings\n      popularSearches {\n        text\n        url\n        __typename\n      }\n      __typename\n    }\n    copyrightYear\n    footerVO {\n      countryMenu {\n        childNavigationLinks {\n          id\n          link\n          textKey\n          __typename\n        }\n        id\n        link\n        textKey\n        __typename\n      }\n      __typename\n    }\n    helpCenterDomain\n    helpCenterLocale\n    isPotentialBot\n    jobAlert {\n      jobAlertExists\n      promptedOnJobsSearch\n      promptingForJobClicks\n      __typename\n    }\n    jobSearchQuery\n    loggedIn\n    searchCriteria {\n      implicitLocation {\n        id\n        localizedDisplayName\n        type\n        __typename\n      }\n      keyword\n      location {\n        id\n        localizedDisplayName\n        shortName\n        localizedShortName\n        type\n        __typename\n      }\n      __typename\n    }\n    showMachineReadableJobs\n    showMissingSearchFieldTooltip\n    __typename\n  }\n  companyFilterOptions {\n    id\n    shortName\n    __typename\n  }\n  pageImpressionGuid\n  pageSlotId\n  relatedCompaniesLRP\n  relatedCompaniesZRP\n  relatedJobTitles\n  resourceLink\n  seoTableEnabled\n  jobListingSeoLinks {\n    linkItems {\n      position\n      url\n      __typename\n    }\n    __typename\n  }\n  jobListings {\n    jobview {\n      job {\n        descriptionFragments\n        eolHashCode\n        jobReqId\n        jobSource\n        jobTitleId\n        jobTitleText\n        listingId\n        __typename\n      }\n      jobListingAdminDetails {\n        adOrderId\n        cpcVal\n        importConfigId\n        jobListingId\n        jobSourceId\n        userEligibleForAdminJobDetails\n        __typename\n      }\n      overview {\n        id\n        name\n        shortName\n        squareLogoUrl\n        __typename\n      }\n      gaTrackerData {\n        trackingUrl\n        jobViewDisplayTimeMillis\n        requiresTracking\n        isIndeedJob\n        searchTypeCode\n        pageRequestGuid\n        isSponsoredFromJobListingHit\n        isSponsoredFromIndeed\n        __typename\n      }\n      header {\n        adOrderId\n        advertiserType\n        ageInDays\n        applyUrl\n        autoLoadApplyForm\n        easyApply\n        easyApplyMethod\n        employerNameFromSearch\n        jobLink\n        jobCountryId\n        jobResultTrackingKey\n        locId\n        locationName\n        locationType\n        needsCommission\n        normalizedJobTitle\n        organic\n        payPercentile90\n        payPercentile50\n        payPercentile10\n        hourlyWagePayPercentile {\n          payPercentile90\n          payPercentile50\n          payPercentile10\n          __typename\n        }\n        rating\n        salarySource\n        sponsored\n        payPeriod\n        payCurrency\n        savedJobId\n        sgocId\n        categoryMgocId\n        urgencySignal {\n          labelKey\n          messageKey\n          normalizedCount\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
# }

# s = requests.session()
# s.headers = HEADERS

# s.get('https://www.glassdoor.com/Job/machine-learning-jobs-SRCH_KO0,16.htm')

# print(s.headers)
# print(s.cookies)

# time.sleep(3)

# r = s.post(
#     url='https://www.glassdoor.com/graph',
#     data=payload,
#     headers=HEADERS
# )

# print(r.reason)