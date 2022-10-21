import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def isSpam(content, spamLinkDomains = [], redirectionDepth = 1):
    # myString = "This is my tweet check it out https://example.com/blah/fsfsfs"
    url = re.search("(?P<url>https?://[^\s]+)", content).group("url")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    for link in soup.find_all('a'):
        if "moimstg.page.link" in link.get('href'):
            print(link.get('href'))
    # print(links)


    if response.history:
        print("Request was redirected")
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a.href')

if __name__ == "__main__":
    isSpam('https://moimstg.page.link/dmCn')