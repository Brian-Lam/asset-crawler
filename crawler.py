import re, urllib
import sys
from urlparse import urlparse
from collections import defaultdict
from os.path import basename
from bs4 import BeautifulSoup, SoupStrainer

# Results of the crawler. This file will list the number of times an asset is used
textfile = file('results_crawler.txt','wt')

# This outputs a list of the sites that were crawled
sites_crawled = file('sites_crawled.txt','wt')

# The domain to be crawled. Will be provided as a parameter
crawl_domain = ""

#Keep track of the pages that are crawled so we don't crawl the same page twice
crawled_pages = []

# Keep track of how many crawls we've made
crawl_count = 0

# The max number of times to crawl. Should be provided as a parameter
max_crawl_count = 10

# If true (provided a parameter), this will output the list of sites crawled
verbose = False

# The dictionary that keeps track of the number of times an asset appears
asset_track = defaultdict(list)

# Crawls the domain and keeps track of asset counts.
def crawl(_page):
    global crawled_pages
    global crawl_count
    global max_crawl_count

    # Do not crawl external domains
    if not _page.startswith(crawl_domain):
        return

    #Skip this page if it has already been crawled
    if _page in crawled_pages:
        return
    else:
        crawled_pages.append(_page)
        

    crawl_count += 1
    if (crawl_count > max_crawl_count):
        raise ValueError('Crawl limit has been reached')
    else:
        print ("Crawling " + _page)
        sites_crawled.write(_page + "\n") 
        print ("(" + str(crawl_count) + "/" + str(max_crawl_count) + ")")


    # Get JS references
    page_open = urllib.urlopen(_page)
    soup = BeautifulSoup(page_open.read())

    # JS Files
    sources = soup.findAll('script', {"src": True})
    for source in sources:
        disassembled = urlparse(str(source["src"]))
        filename = basename(disassembled.path)
        print ("  - Found JS file: " + filename)
        asset_track[filename].append(_page)

    # CSS Files
    css_files = soup.findAll("link", {"rel": "stylesheet"})
    for css_file in css_files:
        disassembled = urlparse(str(css_file["href"]))
        filename = basename(disassembled.path)
        print ("  - Found CSS file: " + filename)
        asset_track[filename].append(_page)

    # Links
    for link in soup.findAll('a'):
        link_url = formaturl(link["href"])
        if not link_url in crawled_pages and link_url.startswith(crawl_domain):
            print "  - Found new link: " + link_url
        try:
            crawl(link_url)
        except IOError as e:
            print ("IOError on " + link_url)
            continue
        except ValueError as err:
            print "Other error"
            continue 

# Format the URL so that BS4 can resolve it properly.  
def formaturl(_url):
    #Append domain to beginning of URL if it isn't already there
    if _url.endswith("/"):
        _url = _url[:-1]
    if not crawl_domain in _url:
        if not "http://" in _url and not "https://" in _url:
            _url = str(crawl_domain + _url)
    return _url.strip()

# Called after crawling has completed. This will output the results
# of the crawl into a file. 
def makereport():
    for asset, refs in asset_track.iteritems():
        # Put in a set to take out duplicates, TODO implement better fix
        refs_set = set(refs)
        textfile.write(asset + " : " + str(len(refs_set)) + " references" + "\n")
        if verbose:
            for ref in refs_set:
                textfile.write("  - " + ref + "\n")
    print "Reported generated to results_crawl.txt"
    print "Sites crawled listed on sites_crawled.txt"
    textfile.close()
    sites_crawled.close()

# Parse the command line arguments to determine script behavior
def init():
    global crawl_domain
    global max_crawl_count
    if len(sys.argv) == 1:
        print "Usage:"
        print "python crawler.py (url) (max-crawl) [-V]"
        print "Options: -v for verbose report"
        print "Example: python crawler.py https://www.brianlam.us"
        print ""
        raise ValueError ("Incorrect usage")
    if len(sys.argv) > 1:
        crawl_domain = sys.argv[1]
        crawl_domain = (crawl_domain + "/") if not crawl_domain.endswith("/") else crawl_domain
    if len(sys.argv) > 2:
        if sys.argv[2] != "-V" and sys.argv[2] != "-v":
            max_crawl_count = sys.argv[2];
    if len(sys.argv) > 3:
        if sys.argv[3] == "-V" and sys.argv[3] == "-v":
            verbose = True

    print ("Crawling domain " + crawl_domain)

# Script entry function
if __name__ == "__main__":
    init()
    try: 
        crawl(crawl_domain)
    except ValueError as err: 
        print(err.args)
    makereport()
