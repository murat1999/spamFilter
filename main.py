import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import asyncio

async def checkLink(response, spamLinkDomains):
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
        print('Detected')
        return True

    # getting an array of urls (redirected and the final destination)
    redirectUrls = []
    for url in response.history[1:]:
        redirectUrls.append(url.url)
    redirectUrls.append(response.url)

    print(redirectUrls)

    if response.history:
        print("Request was redirected")

        for i in range(redirectionDepth):
            if i + 1 <= len(redirectUrls):
                checkingUrl = urlparse(redirectUrls[i]).netloc
                if checkingUrl in spamLinkDomains:
                    print('Spam')
                    return True
                else:
                    subResponce = requests.get(redirectUrls[i])

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(checkLink(subResponce, spamLinkDomains))
            else:
                # for j in range(i + 1, redirectionDepth):
                # checkLink(requests.get(redirectUrls[-1]), spamLinkDomains)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(checkLink(subResponce, spamLinkDomains))


        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(checkLink(subResponce, spamLinkDomains))
    return False

if __name__ == "__main__":
    isSpam('spam spam https://moimstg.page.link/dmCn', ['skills.github.com'], 2)