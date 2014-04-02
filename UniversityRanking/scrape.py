import urlparse
import urllib
from bs4 import BeautifulSoup
import json

url = "http://www.tamu.edu/"

urls = [url] # stack of urls to scrape
visited = [url] # historic record of urls

while len(urls) > 0:
    try:
        htmltext = urllib.urlopen(urls[0]).read()
    except:
        continue
    soup = BeautifulSoup(htmltext)
    
    urls.pop(0)
    print len(urls)
    for tag in soup.findAll('a',href=True):
        tag['href'] = urlparse.urljoin(url,tag['href'])
        #print tag['href']
        if '.tamu.edu' in tag['href'] and tag['href'] not in visited:
            urls.append(tag['href'])
            visited.append(tag['href'])
        if len(tag['href']) > 200:
            break
f = open("data/visited_urls_2.json","w")
json.dump(visited, f)
f.close()