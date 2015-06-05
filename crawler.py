import re, urllib
import sys
from urlparse import urlparse
from collections import defaultdict
from os.path import basename
from bs4 import BeautifulSoup, SoupStrainer

textfile = file('results_crawler.txt','wt')

crawl_domain = "http://www.alexanderinteractive.com/"
crawl_domain = (crawl_domain + "/") if not crawl_domain.endswith("/") else crawl_domain

crawled_pages = []
crawl_count = 0
max_crawl_count = 250
verbose = False

asset_track = defaultdict(list)

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
        print ("Crawling " + _page)

    print ("(" + str(crawl_count) + "/" + str(max_crawl_count) + ")")
    crawl_count += 1
    if (crawl_count > max_crawl_count):
        raise ValueError('Crawl limit has been reached')

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
            if (err.args == "Crawl limit has been reached"):
                raise ValueError(err.args)
        except Exception as e:
            print "Other error"
            continue      

def formaturl(_url):
    #Append domain to beginning of URL if it isn't already there
    if _url.endswith("/"):
        _url = _url[:-1]
    if not crawl_domain in _url:
        if not "http://" in _url and not "https://" in _url:
            _url = str(crawl_domain + _url)
    return _url.strip()

def makereport():
    for asset, refs in asset_track.iteritems():
        # Put in a set to take out duplicates, TODO implement better fix
        refs_set = set(refs)
        textfile.write(asset + " : " + str(len(refs_set)) + " references" + "\n")
        if verbose:
            for ref in refs_set:
                textfile.write("  - " + ref + "\n")
    print "Reported generated to results_crawl.txt"

def init():
    global crawl_domain
    # Command line arguments not 100% working yet
    if len(sys.argv) > 2:
        crawl_domain = sys.argv[1]
    if len(sys.argv) > 3:
        if sys.argv[2] == "-V":
            verbose = True

    print ("Crawling domain " + crawl_domain)


if __name__ == "__main__":
    init()
    try: 
        crawl(crawl_domain)
    except ValueError as err: 
        print(err.args)
    makereport()
    textfile.close()
