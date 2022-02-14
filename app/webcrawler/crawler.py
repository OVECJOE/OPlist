import os
from bs4 import BeautifulSoup
from difflib import get_close_matches
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

from .models.query_model import QueryModel
from .models.table_models import Url, Keyword
from .link_collector import LinkCollector
from .urls_organizer import UrlsOrganizer


class ContentFetcher:
    """
    This class defines an object that gather content from URLs
    based on user's search query.
    """
    __keywords = []
    lc = LinkCollector()

    def __init__(self, **kwargs):
        """Initializes the class"""
        self.__qm = QueryModel(**kwargs)
        self.__supported_kings = {
            "SEARCH": self.search,
            # "FASTSEARCH": self.fastSearch,
            # "ADDURLS": self.addUrls,
        }

        self.__metadata = MetaData()
        user = os.getenv("WC_USER")
        host = os.getenv('WC_HOST')
        passwd = os.getenv('WC_PWD')
        db = os.getenv('WC_DB')
        DATABASE_URL = "postgresql://{}:{}@{}:5432/{}"\
            .format(user, passwd, host, db)
        engine = create_engine(DATABASE_URL)
        self.__metadata.create_all(engine)
        self.__session = sessionmaker(bind=engine)()

    def is_king_supported(self):
        """Checks if the king present in the command_set is supported"""
        king = self.__qm.king
        if king in self.__supported_kings:
            return True
        return False

    def generate_keywords(self):
        """
        Goes into the datasets and generates keywords present in the database
        to speed up query.
        """
        uo = UrlsOrganizer()
        datasets = uo.reload()
        ContentFetcher.__keywords = datasets.keys()

    def is_head_keyword(self):
        """
        Checks if the head of the command set is a keyword that the
        database is aware of
        """
        if self.__qm.head in ContentFetcher.__keywords:
            return True
        else:
            match = get_close_matches(self.__qm.head, self.__keywords,
                                      cutoff=0.7, n=1)
            if match and match[0] in self.__keywords:
                return True
        return False

    def process(self):
        """
        Checks the king and calls the appropriate method to process the
        disciple.
        """
        self.generate_keywords()
        if self.is_king_supported():
            return self.__supported_kings[self.__qm.king]

    def __get_urls(self, head):
        """
        Obtain all urls partaining to a keyword.
        """
        if head not in ContentFetcher.__keywords:
            match = get_close_matches(head, self.__keywords,
                                      cutoff=0.7, n=1)
            if match:
                head = match[0]
        id_ = self.__session.query(Keyword).filter(
            Keyword.name == head).first().id
        results = self.__session.query(Url).filter(
            Url.keyword_id == id_).all()
        return [rec.url for rec in results]

    def __get_title(self, bs: BeautifulSoup):
        """
        Gets the title related to a parsed page
        """
        try:
            title = bs.title.text
        except AttributeError:
            h1_tags = bs.find_all('h1')
            if len(h1_tags) == 1:
                title = h1_tags[0].text
            else:
                for h1 in h1_tags:
                    if h1.has_attr('id') and h1['id'] == 'title':
                        title = h1.text
                        break
                else:
                    title = bs.find(class_='title').text
        return title if title else bs.h1.text

    def __get_body(self, title, body, bs: BeautifulSoup):
        """
        Locates `body` within bs.body
        """
        if body.lower() in title.lower():
            return title
        else:
            text = bs.body.text.lower()
            idx = text.find(body.lower())
            return body.lower() in text and \
                text[idx: idx+len(body)*10]

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

        data = []

        if self.is_head_keyword():
            results = self.__get_urls(head)
            for url in results:
                html = self.lc.getPage(url)
                if html:
                    bs = BeautifulSoup(html, 'html.parser')
                    title = self.__get_title(bs)
                    content = self.__get_body(title, body, bs)
                    data.append((title, f'{content}...', url)) if content else\
                        print("<{}> not found in page with title ({})".format(
                            body, title))
            print(data)
            return data
