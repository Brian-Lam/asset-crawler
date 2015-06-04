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
from urlparse import urlparse
from collections import defaultdict
from os.path import splitext, basename

textfile = file('crawler_results.txt','wt')
crawl_domain = "http://www.alexanderinteractive.com"

crawled_pages = []
crawl_count = 0
max_crawl_count = 50

asset_track = defaultdict(list)

def crawl(_page):
	global crawled_pages
	global crawl_count
	global max_crawl_count

	# Do not crawl external domains
	if not crawl_domain in _page: 
		print ("Skipping URL " + _page)
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

	for link in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(_page).read(), re.I):

	    # Format URL
	    link = formaturl(link)
	    
	    print "  - Found " + link

	    #Skip telephone links, should replace this with a regex later
	    if "tel:" in link:
	    	continue

	    if ".css" in link or ".js" in link:
	    	disassembled = urlparse(str(link))
	    	filename, file_ext = splitext(basename(disassembled.path))
        	asset_track[basename(disassembled.path)].append(_page)
	    # Crawl the links within this given _page
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

	makereport()
	print("Results written to crawl_results.txt")


def formaturl(_url):
    #Append domain to beginning of URL if it isn't already there
    if not crawl_domain in _url:
    	if not "http://" in _url and not "https://" in _url:
	    	_url = str(crawl_domain + _url)
	if _url.endswith("/"):
		_url = _url[:-1]
    return _url.strip()

def makereport():
	for asset, refs in asset_track.iteritems():
		# Put in a set to take out duplicates, TODO implement better fix
		refs_set = set(refs)
		textfile.write(asset + " : " + str(len(refs_set)) + " references" + "\n")
		for ref in refs_set:
			textfile.write("  - " + ref + "\n")

if __name__ == "__main__":
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