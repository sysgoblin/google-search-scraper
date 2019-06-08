# GScrape (WIP)
## Google Search Scraper

Scrapes google so you don't have to.

### Installation
Works in python 3.
Requires the following python packages: 
```sh
pip install -r requirements.txt
```


#### Usage
```
$ python google-search-scraper.py --intext "sysgoblin" --excluded-domains "github.com", "twitter.com" --range month --output-path "/Users/user/Desktop/1.json"
```

#### Params
**--intext** : The text you want to search for. Equivalent to google dork input.

**--excluded-domains** : Comma separated strings of domains to not list results for.

**--range** : Date range to search within. Takes `hour, day, week, month, year, alltime`

**--output-path** : Full path to output json formatted results.

**--proxy** : Proxy requests via 127.0.0.1:8080 (if you use Burp). 

*Note: I haven't been caught by Google's bot detection yet however if you are stopped due to captcha, using this should 
allow you to open the page within your browser and complete the request.

##### To Do
* Replace unicode w/ text
* Allow proxy config customisation
* Clean up code
* Test captcha handling