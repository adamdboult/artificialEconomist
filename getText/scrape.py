#!/usr/bin/env python3
"""
Hi
"""
##########
# IMPORT #
##########

import os

# import urllib.request
# import urllib.parse

import requests
from bs4 import BeautifulSoup

################################
# GET URLS TO SCRAPE: Econstor #
################################

####
# Pre
####
pre_urls_econstor = [
    "https://www.econstor.eu/browse?type=doctype&sort_by=1&order=DESC&rpp=100&etal=-1&value=Working+Paper"
]

urls_econstor = []

for pre_url in pre_urls_econstor:
    for page in range(1, 100):
        start = ((page - 1) * 100) + 0
        new_url = pre_url + "&offset=" + str(start)
        urls_econstor.append(new_url)

####
# Get list of actual URLs
####
second_link_list_econstor = []

for url in urls_econstor:
    response = requests.get(url, stream=True, timeout=10)

    soup = BeautifulSoup(response.text, "lxml")
    for link in soup.find_all("a"):  # Finds all links
        if "/handle" in str(link):  # If the link ends in .pdf
            linkname = "https://www.econstor.eu" + link.get("href")
            second_link_list_econstor.append(linkname)

###########################
# GET URLS TO SCRAPE: FCA #
###########################
pre_urls_fca = [
    # "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-policy%20statements",
    "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-feedback%20statements",
    "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-discussion%20papers",
    # "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-finalised%20guidance",
    # "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-calls%20for%20input",
    "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-consultation%20papers",
    "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-guidance%20consultations",
    # "https://www.fca.org.uk/publications/search-results?np_category=policy%20and%20guidance-newsletters",
    "https://www.fca.org.uk/publications/search-results?np_category=research-market%20studies",
    "https://www.fca.org.uk/publications/search-results?np_category=research-thematic%20reviews",
    "https://www.fca.org.uk/publications/search-results?np_category=research-multi-firm%20reviews",
    "https://www.fca.org.uk/publications/search-results?np_category=research-occasional%20papers",
    "https://www.fca.org.uk/publications/search-results?np_category=research-research",
]

second_link_list_fca = []

for pre_url in pre_urls_fca:
    for page in range(1, 50):
        start = ((page - 1) * 10) + 1
        new_url = pre_url + "&start=" + str(start)
        second_link_list_fca.append(new_url)


########################
# GET URLS TO DOWNLOAD #
########################
def get_link_list(second_link_list):
    """
    Documentation
    """
    link_list = []

    for url in second_link_list:
        response = requests.get(url, stream=True, timeout=10)

        soup = BeautifulSoup(response.text, "lxml")
        for link in soup.find_all("a"):  # Finds all links
            if ".pdf" in str(link):  # If the link ends in .pdf
                if not link.get("href") in link_list:
                    link_list.append(link.get("href"))
        return link_list


link_list_fca = get_link_list(second_link_list_fca)
link_list_econstor = get_link_list(second_link_list_econstor)

#################
# DOWNLOAD PDFs #
#################

# def is_valid_url(url):
#    parsed = urllib.parse.urlparse(url)
#    return parsed.scheme in {"http", "https"}


def download_pdfs(link_list, run_specific_folder):
    """
    Documentation
    """
    hdr = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
    }

    for index, link in enumerate(link_list):

        print(f"Downloading {link}")

        # request = urllib.request.Request(url=link, headers=hdr)
        # request = urllib.request.Request(url=link, headers=hdr)
        response = requests.get(link, headers=hdr, timeout=10)
        content = response.content  # To get the raw response content
        # response = urllib.request.urlopen(request)
        # with urllib.request.urlopen(request) as response:
        #    content = response.read()

        # if is_valid_url(request):
        #    with urllib.request.urlopen(request) as response:
        #        content = response.read()
        # else:
        #    raise ValueError(f"Invalid or unsupported URL scheme: {request}")

        file_path = os.path.join(
            run_specific_folder, f"{run_specific_folder}_{str(index)}.pdf"
        )
        folder_path = os.path.dirname(file_path)
        if folder_path and not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(file_path, "wb", encoding="utf-8") as file:
            file.write(content)


download_pdfs(link_list_fca, run_specific_folder="PDF_FCA")
download_pdfs(link_list_econstor, run_specific_folder="PDF_econstor")
