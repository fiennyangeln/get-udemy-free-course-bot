# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

#class Project1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
class UrlItem(scrapy.Item):
    course_name= scrapy.Field()
    udemy_url = scrapy.Field()
    pass


# from datetime import datetime

engine = create_engine("sqlite:///courses.db")
Base = declarative_base()

class Course(Base):

    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    udemy_url = Column('url',String, default=None, index=True)
    checkout_url = Column(String, default=None, index=True)
    course_name = Column('courseTitle',String, default=None, index=True)
    discounted_price = Column(Integer, default=None, index=True)
    original_price = Column(Integer, default=None, index=True)
    date_last_checked = Column(Date, default=None, index=True)
    status = Column(String, default=None, index=True)
    remarks = Column(String, default=None, index=True)

    #----------------------------------------------------------------------
    def __init__(self, udemy_url, course_name, checkout_url=None, discounted_price=None, original_price=None, date_last_checked=None, status=None, remarks=None):


        self.udemy_url = udemy_url
        self.checkout_url = checkout_url
        self.course_name = course_name
        self.discounted_price = discounted_price
        self.original_price = original_price
        self.date_last_checked = date_last_checked
        self.status = status
        self.remarks = remarks

# create tables
Base.metadata.create_all(engine)
