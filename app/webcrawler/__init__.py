from urls_organizer import UrlsOrganizer
from link_collector import LinkCollector

collectedLinks = []
visitedLinks = []

lc = LinkCollector()
uo = UrlsOrganizer(collectedLinks, visitedLinks)


def crawl_and_save():
    while True:
        if collectedLinks:
            seedURLs = [result[1] for result in collectedLinks]
        else:
            seedURLs = []
        lc.loopThruSeedUrls(seedURLs)
        collectedLinks = lc.collectedLinks
        visitedLinks.extend(lc.visitedLinks)
        uo.save()
