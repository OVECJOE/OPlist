import os
from bs4 import BeautifulSoup
from difflib import get_close_matches
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

from models.query_model import QueryModel
from models.table_models import Url, Keyword
from webcrawler import uo, lc


class ContentFetcher:
    """
    This class defines an object that gather content from URLs
    based on user's search query.
    """
    __keywords = None

    def __init__(self, command_set: list):
        """Initializes the class"""
        d = {
            "king": command_set[0],
            "head": command_set[1],
            "body": command_set[2]
        }
        self.__qm = QueryModel(**d)
        self.__supportedKings = {
            "SEARCH": self.search,
            "FASTSEARCH": self.fastSearch,
            "ADDURLS": self.addUrls,
        }

        self.__metadata = MetaData()
        user = os.getenv("WC_USER")
        host = os.getenv('WC_HOST')
        passwd = os.getenv('WC_PWD')
        db = os.getenv('WC_DB')
        DATABASE_URL = "mysql+mysqldb://{}:{}@{}:3306/{}"\
            .format(user, passwd, host, db)
        engine = create_engine(DATABASE_URL)
        self.__metadata.create_all(engine)
        self.__session = sessionmaker(bind=engine)()

    def isKingSupported(self):
        """Checks if the king present in the command_set is supported"""
        king = self.__qm.king
        if king in self.__supportedKings:
            return True
        return False

    def generateKeywords(self):
        """
        Goes into the datasets and generates keywords present in the database
        to speed up query.
        """
        datasets = uo.reload()
        ContentFetcher.__keywords = datasets.keys()

    def isHeadAKeyword(self):
        """
        Checks if the head of the command set is a keyword that the
        database is aware of
        """
        if self.__qm.head in self.__keywords:
            return True
        else:
            match = get_close_matches(self.__qm.head, self.__keywords,
                                      cutoff=0.8, n=1)
            if match and match[0] in self.__keywords:
                return True
        return False

    def process(self):
        """
        Checks the king and calls the appropriate method to process the
        disciple.
        """
        self.generateKeywords()
        if self.isKingSupported():
            return self.__supportedKings[self.__qm.king]
        return AttributeError(
            f"'{self.__qm.king}' is not a valid opcode!")

    def search(self):
        """
        Mapped to the 'SEARCH' king. It works simply like how almost
        every search query's result works. Queries the database for the
        head and then proceed to gather information based on the URLs returned
        for that keyword, if it exists.

        Guess what? In here, I disobeyed a zen of Python. To find out,
        try this:
            >>> import this
        """
        head = self.__qm.head
        body = self.__qm.body

        if self.isHeadAKeyword():
            id_ = self.__session.query(Keyword).filter(
                Keyword.name == head).first().id
            results = self.__session.query(Url).filter(
                Url.keyword_id == id_).all()
            results = [rec.url for rec in results]

            for url in results:
                html = lc.getPage(url)
                if html:
                    bs = BeautifulSoup(html, 'html5lib')