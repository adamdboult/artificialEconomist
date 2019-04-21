##########
# IMPORT #
##########

import requests
from bs4 import BeautifulSoup
import shutil


import os
    
bs = BeautifulSoup

import urllib.request

######################
# GET URLS TO SCRAPE #
######################
preURL = "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-policy%20statements"

URLs = []

for page in range(1, 150):
    start = ((page - 1) * 10) + 1
    newURL = preURL + "&start=" + str(start)
    URLs.append(newURL)

print("\n".join(URLs))
#print (URLs)

########################
# GET URLS TO DOWNLOAD #
########################
link_list = []

for URL in URLs:
    response = requests.get(URL, stream=True)

    soup = bs(response.text)
    for link in soup.find_all('a'): # Finds all links
        if ".pdf" in str(link): # If the link ends in .pdf
            link_list.append(link.get('href'))

print("\n".join(link_list))
#print(link_list)

#################
# DOWNLOAD PDFs #
#################
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

if not os.path.exists("PDF/"):
    os.makedirs("PDF/")

i = 1
for link in link_list:

    #print (link)
    
    request = urllib.request.Request(url=link, headers=hdr)
    response = urllib.request.urlopen(request)
    
    file = open("PDF/" + str(i) + ".pdf", "wb")
    file.write(response.read())
    file.close()
    i = i + 1
