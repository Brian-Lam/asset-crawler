"""
	Asset crawler
	Author: Brian Lam

	This will crawl a website and report how often a .js or .css file is
	used, and what pages it's used on. Developed while interning at 
	Alexander Interactive. 

	Initial templating:
	http://null-byte.wonderhowto.com/inspiration/basic-website-crawler-python-12-lines-code-0132785/
"""

import re, urllib
from collections import defaultdict

textfile = file('crawler_results.txt','wt')
crawl_domain = "http://www.alexanderinteractive.com"

crawled_pages = []
crawl_count = 0
max_crawl_count = 0

asset_track = defaultdict(list)

def crawl(_url):
	global crawled_pages
	global crawl_count
	global max_crawl_count

	# Do not crawl external domains
	if not crawl_domain in _url: 
		print ("Skipping URL " + _url)
		return

	#Skip this page if it has already been crawled
	if _url in crawled_pages:
		return
	else:
		crawled_pages.append(_url)
		print ("Crawling " + _url)

	crawl_count += 1
	if (crawl_count > max_crawl_count):
		return	

	for link in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(_url).read(), re.I):
	    
	    print "  - Found " + link

	    # Format URL
	    link = formaturl(link)

	    #Skip telephone links, should replace this with a regex later
	    if "tel:" in link:
	    	continue

	    # Crawl the links within this given _url
	    try: 
		    for ee in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(link).read(), re.I):
		    	ee = formaturl(ee)
		        if ".css" in ee or ".js" in ee:
		        	asset_track[ee].append(link)
		        if crawl_domain in ee:
			        crawl(ee)
	    except IOError as e:
			print ("IOError on " + link)
			continue
	    except Exception:
			print "Other error"
			continue

	for asset, refs in asset_track.iteritems():
		textfile.write(asset + " : " + len(refs) + " references")
		for ref in refs:
			textfile.write("  - " + ref + "\n")

	textfile.close()
	print("Results written to crawl_results.txt")


def formaturl(_url):
    #Append domain to beginning of URL if it isn't already there
    if not crawl_domain in _url:
    	if not "http://" in _url and not "https://" in _url:
	    	_url = str(crawl_domain + _url)
    return _url.strip()

if __name__ == "__main__":
    crawl(crawl_domain)

"""
TODO
	Custom grouping (/blogs directory)
	Regex for telephone, css, and js
	Only crawl on specified domain
	Call this recursively for a multi-level call
"""