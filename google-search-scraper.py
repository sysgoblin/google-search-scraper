# results 1-100
# site : https://www.google.com/search?q=
# dork: intext:"secure+trust+bank"+-site:securetrustbank.com
# number of results per page: &num=100
# what number to start at: &start=0
# time range enforces sort by relevance
# all time: &tbas=0
# past week only: &tbs=qdr:w
# past month: &tbs=qdr:m
# past year: &tbs=qdr:y
# past hour: &tbs=qdr:h
# custom range: (text) tbs=cdr:1,cd_min:1/10/2019,cd_max:1/26/2019 (url encoded) tbs=cdr%3A1%2Ccd_min%3A1%2F10%2F2019%2Ccd_max%3A1%2F26%2F2019
# verbatim search: &tbs=li

import requests
import time
import random
import decimal
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


results_obj = {}
textdork = 'by v12 retail finance'
excluded_domains = ['securetrustbank.com',
                    'linkedin.com',
                    'telegraph.co.uk',
                    'totaljobs.com',
                    'v12finance.com',
                    'fca.org.uk',
                    'trustpilot.com',
                    'feefo.com',
                    'companieshouse.gov.uk',
                    'moneysavingexpert.com',
                    'indeed.co.uk',
                    'yell.com',
                    'reed.co.uk']
textdork_str = 'intext:' + '"' + textdork.replace(' ', '+') + '"'
random.shuffle(excluded_domains)
excluded_domains_str = ''
for d in excluded_domains:
    excluded_domains_str += '+-site:' + d

useragent = UserAgent()

hr = '&tbs=qdr:h'
day = '&tbs=qdr:d'
week = '&tbs=qdr:w'
month = '&tbs=qdr:m'
year = '&tbs=qdr:y'
alltime = '&tbas=0'
startnum = 0

requests.packages.urllib3.disable_warnings()
rem = True

referrer = 'https://www.google.com'
page = 1

while rem:
    # get cookies (nom)
    session = requests.session()
    response = session.get('http://google.com')
    cookies = session.cookies.get_dict()

    # set default headers
    headers = {'user-agent': useragent.random,
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Referer': referrer,
               'Upgrade-Insecure-Requests': '1'
               }
    # add cookies to headers
    for k, v in cookies.items():
        headers[k] = v

    url = 'https://www.google.com/search?q=' + textdork_str + excluded_domains_str + '&num=100' + week + '&start=' + str(
        startnum)

    req = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(req.content, "html.parser")

    # links only
    resultbody = soup.find('div', {'id': 'search'})
    links = resultbody.find_all('a', href=True)

    if len(resultbody) >= 1:
        results = []

        for l in links:
            # improve this
            # if any(x not in l['href'] for x in ['webcache', '#']):
            if 'webcache' not in l['href'] and '#' not in l['href'] and '?q=related:' not in l['href']:
                results.append(l['href'])

        # links n titles/desc
        sections = resultbody.find_all('div', {'class': 'rc'})

        for section in sections:
            href = section.find('a')['href']
            parsed_domain = urlparse(href)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_domain)
            title = section.find('h3').text
            desc = section.find('span', {'class': 'st'}).text

            info = {'URL': href,
                    'Title': title,
                    'Text': desc,
                    'Page': page
                    }

            results_obj[domain] = info

    else:
        rem = False

    if rem is True:
        print("Moving to next page")

    page += 1
    startnum += 100
    referrer = str(url)
    randomwait = float(decimal.Decimal(random.randint(80,250)/100)) # time between 0.8 seconds and 2.5
    time.sleep(randomwait)

print(json.dumps(results_obj, indent=4))