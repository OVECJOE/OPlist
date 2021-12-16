from datetime import datetime
from urllib.error import URLError
from urllib.parse import urlparse
import requests
from requests.exceptions import ConnectionError, InvalidURL
from bs4 import BeautifulSoup
import re


class LinkCollector:
    """
    A link collector class that crawls through the internet and obtain
    content-related links
    """

    def __init__(self, title=""):
        """Initializes the link collector object/instance"""
        self.title = title
        self.__seedURLs = [
            'https://www.codementor.io/projects',
            'https://www.geeksforgeeks.org/',
            'https://www.freecodecamp.org/learn/',
            'https://www.w3schools.com/',
            'https://developer.mozilla.org/en-US/'
        ]
        self.gatheredLinks = []
        self.__urlPattern = re.compile(r'^((http(s)?)://)(www.)?\S+')
        self.__count = 0

    def getPage(self, url):
        """Gets the web page of a url containing the code."""
        try:
            newUrl = "{}://{}".format(urlparse(url).scheme,
                                      urlparse(url).netloc)
            response = requests.get(newUrl, allow_redirects=True)
            if response.status_code == 200:
                return response.text
        except (ConnectionError, InvalidURL) as e:
            print("Error:", e)
        except KeyboardInterrupt:
            print('\n\n', self.gatheredLinks)

    def parsePage(self, url):
        """Uses BeautifulSoup to parse the html page loaded"""
        self.__count += 1
        print("Targeting url ({}) at {} --- [{:d}]".
              format(url, datetime.now(), self.__count))
        html = self.getPage(url)
        if html is None:
            return
        links = []
        bs = BeautifulSoup(html, 'html.parser')
        for link in bs.findAll('a'):
            if 'href' in link.attrs and link not in links:
                links.append(link.attrs['href'])
        for link in links:
            if self.__urlPattern.match(link):
                link = "{}://{}{}".format(
                    urlparse(link).scheme,
                    urlparse(link).netloc,
                    urlparse(link).path
                )
                if link not in self.gatheredLinks:
                    self.gatheredLinks.append(link)
            else:
                newUrl = "{}://{}".format(urlparse(url).scheme,
                                          urlparse(url).netloc) + link
                if newUrl not in self.gatheredLinks:
                    self.gatheredLinks.append(newUrl)

    def loopThruSeedUrls(self, seedUrls=[]):
        """Goes through all the seed URLs and extract links"""
        if len(seedUrls) > 0:
            self.__seedURLs = seedUrls
        for url in self.__seedURLs:
            self.parsePage(url)


# if __name__ == '__main__':
#     link_collector = LinkCollector()
#     link_collector.loopThruSeedUrls()
#     links = link_collector.gatheredLinks
#     print(len(links))
#     link_collector.loopThruSeedUrls(links)
#     print(len(link_collector.gatheredLinks))
