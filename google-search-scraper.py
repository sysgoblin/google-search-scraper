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
# GOOGLE_ABUSE_EXEMPTION=ID=cb4524e307d40a7a:TM=1559492993:C=r:IP=212.159.103.86-:S=APGng0vzUUQOALhaz4KzUZF3KJXhe2xycQ

import requests
import time
import random
import decimal
import json
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

parser = argparse.ArgumentParser(description="google scraper", usage='bleh')
parser.add_argument('--intext', required=True, type=str, help='string to search for')
parser.add_argument('--excluded_domains', required=False,  nargs='+', help='domains to exlude from results')
parser.add_argument('--range', required=True, choices=['hr', 'day', 'week', 'month', 'year', 'alltime'], default='alltime')
parser.add_argument('--output_path', required=False, )

args = parser.parse_args()
print(args)

def main():

    # set arg values
    textdork = args.intext
    if args.excluded_domains:
        excluded_domains = args.excluded_domains

        random.shuffle(excluded_domains)

        excluded_domains_str = ''
        for d in excluded_domains:
            excluded_domains_str += '+-site:' + d

    textdork_str = 'intext:' + '"' + textdork.replace(' ', '+') + '"'

    if args.range:
        range_dict = {
        "hr" : '&tbs=qdr:h',
        "day" : '&tbs=qdr:d',
        "week" : '&tbs=qdr:w',
        "month" : '&tbs=qdr:m',
        "year" : '&tbs=qdr:y',
        "alltime" : '&tbas=0',
        }

        range = range_dict[args.range]
    else:
        range = '&tbas=0'

    # set some other values
    requests.packages.urllib3.disable_warnings()
    useragent = UserAgent()
    results_obj = {}
    referrer = 'https://www.github.com/'
    page = 1
    startnum = 0

    rem = True

    while rem:
        # get cookies (nom)
        session = requests.session()
        response = session.get('http://google.com')
        print(response)
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

        # construct url
        url = 'https://www.google.com/search?q=' + textdork_str

        if args.excluded_domains:
            url = url + excluded_domains_str

        url = url + '&num=100' '&start=' + str(startnum) + range

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
        randomwait = float(decimal.Decimal(random.randint(80,250)/100)) # random time between 0.8 seconds and 2.5
        time.sleep(randomwait)

    print(json.dumps(results_obj, indent=4))

    if args.output_path:
        f = open( args.output_path, 'w')
        f.write(json.dumps(results_obj, indent=4))
        f.close


if __name__ == '__main__':
    main()
