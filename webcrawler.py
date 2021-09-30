from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www8.gsb.columbia.edu"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url] # stack of urls seen so far
opened = []

# 2 questions:
# 1. is the page under the CBS domain?
# 2. have we seen this page before?


maxNumUrl = 10; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url = urls.pop(0) # remove the url at index 0
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  # creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): # find tags with links
        childUrl = tag['href']  # extract just the link
        o_childurl = childUrl  # original child url

        #childUrL = www.federalreserve.gov
        #seed_url = www8.gsb.columbia.edu
        # for the above urls, the childUrl below will be the same as before because there is nothing common between them
        # but if the childUrl = /about.html, the childUrl after the urljoin below will be www8.gsb.columbia.edu/about.html

        childUrl = urllib.parse.urljoin(seed_url, childUrl)  # we only want urls that are in the same domain as cbs
        print("seed_url=" + seed_url)
        print("original childurl=" + o_childurl)
        print("childurl=" + childUrl)
        print("seed_url in childUrl=" + str(seed_url in childUrl))
        print("Have we seen this childUrl=" + str(childUrl in seen))
        if seed_url in childUrl and childUrl not in seen:  # we only want urls that are in the same domain as cbs
            print("***urls.append and seen.append***")
            urls.append(childUrl)
            seen.append(childUrl)
        else:
            print("######")

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))

print("List of seen URLs:")
for seen_url in seen:
    print(seen_url)