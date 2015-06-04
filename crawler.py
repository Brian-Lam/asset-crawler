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
asset_track = defaultdict(list)

def crawl(_url):
	if not crawl_domain in _url: 
		return
	if _url in crawled_pages:
		return
	else:
		crawled_pages.append(_url)

	for i in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(_url).read(), re.I):
	    print "Crawling " + i

	    #format
	    i = formaturl(i)

	    #Skip telephones, should replace this with a regex later
	    if "tel:" in i:
	    	continue

	    for ee in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(i).read(), re.I):
	    	ee = formaturl(ee)
	        if ".css" in ee or ".js" in ee:
	        	asset_track[ee].append(i)
	        if crawl_domain in ee:
	        	print "Will crawl" + ee
		        crawl(ee)

	for asset, refs in asset_track.iteritems():
		print asset
		for ref in refs:
			print "  - " + ref

def formaturl(_url):
    #Append domain to beginning of URL if it isn't already there
    if not crawl_domain in _url:
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