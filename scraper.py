import requests
from bs4 import BeautifulSoup as bs

URL = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=software+engineer+intern&locT=C&locId=1147056&jobType=&context=Jobs&sc.keyword=software+engineer+intern&dropdown=0"
page = requests.get(URL)

soup = bs(page.content, 'html.parser')


print(soup)
