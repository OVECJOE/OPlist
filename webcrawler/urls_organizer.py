"""
Contains the class implementation, UrlsOrganizer, to organize the links
gathered based on keywords and save them into a database.
"""
from time import sleep
import yake

from link_collector import LinkCollector


class UrlsOrganizer:
    """Organizes URLs based on keywords"""

    def __init__(self, seedUrls=None):
        lc = LinkCollector()
        print("Step #1: Gathering links...\n\n")
        sleep(5)
        lc.loopThruSeedUrls(seedUrls)
        self.__collectedLinks = lc.collectedLinks
        self.__visitedLinks = lc.visitedLinks
        self.__datasets = {}

    def __extractImportantKws(self):
        """
        It extracts important keywords from the titles of the
        extracted URLs.
        """
        kw_extractor = yake.KeywordExtractor(lan="en", n=1,
                                             dedupLim=.5, top=50,
                                             features=None)
        wordList = " ".join(result[0] for result in self.__collectedLinks)
        keywords = kw_extractor.extract_keywords(wordList)
        return (keyword[0] for keyword in keywords)

    def organize(self):
        """Organize URLs based on keywords into a dict object."""
        keywords = self.__extractImportantKws()

        for keyword in sorted(keywords):
            for link in self.__visitedLinks:
                if keyword in link.split()[-1]:
                    if keyword in self.__datasets:
                        if link in self.__datasets[keyword]:
                            self.__datasets[keyword][
                                self.__datasets[keyword].index(link)] = \
                                {'url': link, 'visited': True}
                        else:
                            self.__datasets[keyword].append(link)
                    else:
                        self.__datasets[keyword] = [link, ]

            for result in self.__collectedLinks:
                if keyword in result[0]:
                    if keyword in self.__datasets:
                        if result[1] not in self.__datasets[keyword]:
                            self.__datasets[keyword].append(result[1])
                    else:
                        self.__datasets[keyword] = [result[1], ]

        return self.__datasets

    def save(self):
        """Saves the result into a database"""
        pass
