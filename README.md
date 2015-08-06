# asset-crawler
This will crawl a website and report how often a .js or .css file is used, and what pages it's used on. Still in development. 

This was developed while I was working at [Alexander Interactive].

## Requirements
This project uses the [Beautiful Soup 4] library. 

Linux package manager: `apt-get install python-bs4`

Pip: `easy_install beautifulsoup4`



## Usage
`python crawler.py (url) (max-crawl) [-v]`
* (url) specifies the URL tto be crawled. This should be inputted with the protocol (http:// or https://) in the beginning. 
* (max-crawl) is the number of crawls the script should make. The script will currently list sites beyond that number, but it will not actually crawl them. 
* [-v] speciifies whether a verbose output file should be create d



[Alexander Interactive]:http://alexanderinteractive.com/
[Beautiful Soup 4]:http://www.crummy.com/software/BeautifulSoup/