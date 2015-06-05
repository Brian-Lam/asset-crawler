import re, urllib
import sys
from urlparse import urlparse
from collections import defaultdict
from os.path import basename
from bs4 import BeautifulSoup

textfile = file('results_crawler.txt','wt')

crawl_domain = "http://www.alexanderinteractive.com/"
crawl_domain = (crawl_domain + "/") if not crawl_domain.endswith("/") else crawl_domain

crawled_pages = []
crawl_count = 0
max_crawl_count = 3500
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
    sources = soup.findAll('script', {"src": True})
    for source in sources:
        disassembled = urlparse(str(source["src"]))
        print ("  - Found JS file: " + str(disassembled))
        asset_track[basename(disassembled.path)].append(_page)

    # This will take care of hrefs (CSS and html page references)
    for link in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(_page).read(), re.I):
        # Format URL
        link = formaturl(link)
        
        print "  - Found " + link

        #Skip telephone links, should replace this with a regex later
        if "tel:" in link:
            continue

        if ".css" in link:
            # The same file might be handled by different subdomains on a CDN
            # Only track by filename
            disassembled = urlparse(str(link))
            asset_track[basename(disassembled.path)].append(_page)
        # Crawl the links within this given _page
        else:
            try: 
                   crawl(link)
            except IOError as e:
                print ("IOError on " + link)
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

global crawl_domain
if __name__ == "__main__":
    # Command line arguments not 100% working yet
    if len(sys.argv) > 2:
        crawl_domain = sys.argv[1]
    if len(sys.argv) > 3:
        if sys.argv[2] == "-V":
            verbose = True
    print ("Crawling domain " + crawl_domain)

    try: 
        crawl(crawl_domain)
    except ValueError as err: 
        print(err.args)
    makereport()
    textfile.close()


"""
TODO
    Custom grouping (/blogs directory)
    Regex for telephone, css, and js
    Only crawl on specified domain
    Call this recursively for a multi-level call
"""