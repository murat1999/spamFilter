import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def checkLink(response, spamLinkDomains):
    domainList = []
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        domain = urlparse(link.get('href')).netloc
        if domain:
            domainList.append(domain)
    for spamLink in spamLinkDomains:
        if spamLink in domainList:
            print(spamLink, 'Spam link detected')
            return True

def isSpam(content, spamLinkDomains, redirectionDepth):
    url = re.search("(?P<url>https?://[^\s]+)", content).group("url")

    response = requests.get(url)
    if urlparse(url).netloc in spamLinkDomains:
        print('YESS')
        return True

    redirectUrls = []
    for url in response.history[1:]:
        redirectUrls.append(url.url)
    redirectUrls.append(response.url)

    print(redirectUrls)

    if response.history:
        print("Request was redirected")

        # if redirectionDepth <= len(redirectUrls):
        for i in range(redirectionDepth):
            if i + 1 <= len(redirectUrls):
                checkingUrl = urlparse(redirectUrls[i]).netloc
                if checkingUrl in spamLinkDomains:
                    print('MURAT')
                    return True
                # subResponce = requests.get(redirectUrls[i])
                # checkLink(subResponce, spamLinkDomains)
            else:
                # for j in range(i + 1, redirectionDepth):
                checkLink(requests.get(redirectUrls[-1]), spamLinkDomains)


        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
        # print(False)
    else:
        checkLink(response, spamLinkDomains)
    return False

if __name__ == "__main__":
    isSpam('spam spam https://moimstg.page.link/dmCn', ['skills.github.com'], 1)