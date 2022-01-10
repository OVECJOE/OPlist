from datetime import datetime
from sqlalchemy import (Column, Integer, VARCHAR, ForeignKey, Boolean,
                        DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Keyword(Base):
    """Models the database table containing keywords"""
    __tablename__ = "keywords"

    id = Column('id', Integer(), primary_key=True, autoincrement=True,
                unique=True, nullable=False)
    name = Column('name', VARCHAR(128), nullable=False, unique=True,
                  index=True)
    no_of_urls = Column('urls_count', Integer(), nullable=False)
    created_on = Column('created_on', DateTime(), default=datetime.now)
    updated_on = Column('updated_on', DateTime(), default=datetime.now,
                        onupdate=datetime.now)
    links = relationship('Url', back_populates='keyword')

    def __repr__(self):
        """Object representation of an instance of this class"""
        return "Keyword(id={:d}, name='{:s}', no_of_urls={:d},".format(
            self.id, self.name, self.no_of_urls) + \
            " created_on={}, updated_on={})".format(self.created_on,
                                                    self.updated_on)

    def __str__(self):
        """
        String representation of the object
        format: (Keyword) [<id>] [<name>]
        """
        return "(Keyword) [{:d}] [{:s}]".format(self.id, self.name)


class Url(Base):
    """Models the database table containing URLs"""
    __tablename__ = "urls"

    id = Column('id', Integer(), primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    keyword_id = Column('keyword_id', ForeignKey('keywords.id'))
    url = Column('url', VARCHAR(256), nullable=False)
    visited = Column('been_visited', Boolean(), nullable=False)
    keyword = relationship('Keyword', back_populates='links',
                           cascade='all, delete')

    def __repr__(self):
        """Object representation of an instance of this class"""
        return "Url(id={:d}, keyword_id={:d}, url='{:s}', visited={})".format(
            self.id, self.keyword_id, self.url, self.visited)

    def __str__(self):
        """
        String representation of an instance of this class
        format: (Url) [<id>] [<url>] | <keyword_id>
        """
        return "(Url) [{:d}] [{:s}] | {:d}".format(
            self.id, self.url, self.keyword_id)
