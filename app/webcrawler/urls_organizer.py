"""
Contains the class implementation, UrlsOrganizer, to organize the links
gathered based on keywords and save them into a database.
"""
import os
from time import sleep
import yake
import json

from link_collector import LinkCollector


class UrlsOrganizer:
    """Organizes URLs based on keywords"""

    __filename = 'json/datasets.json'
    __datasets = {}

    def __init__(self, collectedLinks, visitedLinks):
        self.__collectedLinks = collectedLinks
        self.__visitedLinks = visitedLinks

    def __extractImportantKws(self):
        """
        It extracts important keywords from the titles of the
        extracted URLs.
        """
        kw_extractor = yake.KeywordExtractor(lan="en", n=1,
                                             dedupLim=.4, top=50,
                                             features=None)
        wordList = " ".join(result[0].lower()
                            for result in self.__collectedLinks)
        keywords = kw_extractor.extract_keywords(wordList)
        return (keyword[0].lower() for keyword in keywords)

    def organize(self):
        """Organize URLs based on keywords into a dict object."""
        keywords = self.__extractImportantKws()

        print("Storing links to a dict object...")

        for keyword in sorted(keywords):
            for link in self.__visitedLinks:
                state = {'url': link, 'visited': True}
                if keyword in link.split()[-1].lower():
                    if keyword in self.__datasets:
                        if link in self.__datasets[keyword]:
                            self.__datasets[keyword][
                                self.__datasets[keyword].index(link)] = state
                        else:
                            self.__datasets[keyword].append(state)
                    else:
                        self.__datasets[keyword] = [state, ]

            for result in self.__collectedLinks:
                if keyword in result[0].lower():
                    if keyword in self.__datasets:
                        if result[1] not in self.__datasets[keyword]:
                            self.__datasets[keyword].append(result[1])
                    else:
                        self.__datasets[keyword] = [result[1], ]
        self.__saveAsJson(self.__datasets)
        return self.__datasets.copy()

    def __saveAsJson(self, datasets):
        """Save it to a JSON file as cache"""
        with open(self.__filename, 'w', encoding='uft-8') as jsonfile:
            json.dump(datasets, jsonfile, indent=4)

    def save(self):
        """Saves the result into a database"""
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine
        from sqlalchemy_utils import database_exists, create_database
        from sqlalchemy.inspection import inspect

        from models.table_models import Keyword, Url, Base

        datasets = self.organize()

        print("Storing records into database...")

        user = os.getenv('WC_USER')
        host = os.getenv('WC_HOST')
        passwd = os.getenv('WC_PWD')
        db = os.getenv('WC_DB')

        DATABASE_URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            user, passwd, host, db
        )
        engine = create_engine(DATABASE_URL, echo=True)
        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()

        obj_as_dict = lambda obj: {o.key: getattr(obj, o.key)
            for o in inspect(obj).mapper.column_attrs}

        for key, value in datasets.items():
            stmt = session.query(Keyword).filter(Keyword.name == key).first()
            if stmt is None:
                new_keyword = Keyword(name=key, no_of_urls=0)
            else:
                row = obj_as_dict(stmt)
                new_keyword = session.query(Keyword).get(row['id'])

            for link in value:
                if type(link) is dict:
                    url, visited = link['url'], link['visited']
                else:
                    url, visited = link, False
                stmt = session.query(Url).join(Keyword).filter(
                    Url.keyword_id == new_keyword.id).all()
                records = [rec.url for rec in stmt]

                if url not in records:
                    new_link = Url(url=url, visited=visited)
                    new_keyword.no_of_urls += 1
                    new_link.keyword = new_keyword
                    new_keyword.links.append(new_link)
                    session.add(new_keyword)
                    session.add(new_link)
        session.commit()

    def reload(self) -> dict:
        """Reload the datasets stored in the JSON file."""
        if not os.access(self.__filename, os.F_OK):
            return None
        with open(self.__filename, "r", encoding="utf-8") as jsonfile:
            self.__datasets = json.load(jsonfile)
            return self.__datasets.copy()
