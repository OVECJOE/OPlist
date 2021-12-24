from datetime import datetime
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

    def __init__(self):
        """Initializes the link collector object/instance"""
        self.__seedURLs = [
            'https://www.codementor.io/projects',
            'https://www.geeksforgeeks.org',
            'https://www.freecodecamp.org/learn',
            'https://www.w3schools.com',
            'https://developer.mozilla.org/en-US',
            'https://codeforgeek.com',
            'https://www.fullstackpython.com',
            'https://github.com',
            'https://dev.to',
            'https://blog.feedspot.com/programming_blogs'
        ]
        self.__collectedLinks = set()
        self.__visitedLinks = set()
        self.__urlPattern = re.compile(r'^((http(s)?)://)(www.)?\S+')
        self.__count = 0

    @property
    def collectedLinks(self):
        return self.__collectedLinks
    
    @property
    def visitedLinks(self):
        return self.__visitedLinks

    def getPage(self, url):
        """Gets the web page of a url containing the code."""
        try:
            response = requests.get(url, allow_redirects=True)
            if response.status_code == 200:
                self.__visitedLinks.add(response.url)
                return response.text
        except (ConnectionError, InvalidURL):
            print("Couldn't collect links from {}. I would try another URL..."
                  .format(url))
        except KeyboardInterrupt:
            print("============RESULT=============\n")
            for result in self.__collectedLinks:
                print("\t{}".format(result[0]))
                print("\t\t{}".format(result[1]))
            print("\n\nI am smart. I collected {} links and visited {} URLs!"
                  .format(len(self.__collectedLinks), len(self.__visitedLinks)))

    def __extractPageTitle(self, link):
        """Extracts the page's title for indexing purpose, maybe."""
        html = self.getPage(link)
        if html is not None:
            print("Extracting title from webpage (location: {}, time: {})"
                  .format(link, datetime.now().strftime("%H:%M:%S")))
            bs = BeautifulSoup(html, 'html.parser')
            try:
                title = bs.head.title.text
                return title
            except AttributeError:
                title = bs.title.text
                return title if title else ""

    def __checkLink(self, link):
        """Checks that certain requirements are met for a link"""
        if link in self.__visitedLinks and \
                link in self.__collectedLinks:
            print("Removing link ({})...".format(link))
            self.__collectedLinks.discard(link)

        nonDuplicates = [tup[1] for tup in self.__collectedLinks]
        if self.getPage(link) is not None and link not in nonDuplicates:
            title = self.__extractPageTitle(link)
            print("Adding ({}, {}) to the list of collected links..."
                  .format(title, link))
            self.__collectedLinks.add((title, link, datetime.now()))

    def parsePage(self, url):
        """Parses the html page returned by getPage and stores it as a dict"""
        self.__count += 1
        print("Targeting url ({}) at {} --- [{:d}]".format(
            url,
            datetime.now().
            strftime('Date: %d %b, %Y; Time: %H:%M:%S'),
            self.__count))
        html = self.getPage(url)
        if html is not None:
            print("Parsing Page...")
            bs = BeautifulSoup(html, 'html.parser')
            for a in bs.findAll('a'):
                if all(['href' in a.attrs,
                       a.attrs.get('href', '')
                        not in [tup[1] for tup in self.__collectedLinks]]):
                    link = a.attrs['href']
                    if self.__urlPattern.match(link):
                        link = "{}://{}{}".format(
                            urlparse(link).scheme,
                            urlparse(link).netloc,
                            urlparse(link).path
                        )
                    else:
                        link = "{}://{}".format(urlparse(url).scheme,
                                                urlparse(url).netloc) + link
                    self.__checkLink(link)

    def loopThruSeedUrls(self, seedUrls=[]):
        """Goes through all the seed URLs and extract links"""
        if len(seedUrls) > 0:
            self.__seedURLs = seedUrls
        for url in self.__seedURLs:
            self.parsePage(url)
