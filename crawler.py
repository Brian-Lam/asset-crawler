"""
	Asset crawler
	Author: Brian Lam

	This will crawl a website and report how often a .js or .css file is
	used, and what pages it's used on. Developed while interning at 
	Alexander Interactive. 

	Used this as a starting template:
	http://null-byte.wonderhowto.com/inspiration/basic-website-crawler-python-12-lines-code-0132785/
"""

import re, urllib
from collections import defaultdict

textfile = file('crawler_results.txt','wt')
myurl = "http://www.alexanderinteractive.com"
asset_track = defaultdict(list)

for i in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(myurl).read(), re.I):
    print "Crawling " + i

    #Append domain to beginning of URL if it isn't already there
    if not myurl in i:
    	i = myurl + i

    #Skip telephones, should replace this with a regex later
    if "tel:" in i:
    	continue

    for ee in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(i).read(), re.I):
        if ".css" in ee or ".js" in ee:
        	asset_track[ee].append(i)
"""
TODO
	Regex for telephone, css, and js
	Only crawl on alexanderinteractive.com domain
	Call this recursively for a multi-level call
"""