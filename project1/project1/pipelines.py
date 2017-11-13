# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from project1.items import Course

class UdemyCoursePipeline(object):
    def __init__(self):

        engine = create_engine('sqlite:///courses.db')
        self.Session = sessionmaker(bind=engine)
        #session = Session()


    def process_item(self, item, spider):

        session = self.Session()


        try:
            #try to get the entry in DB that has similar udemy_url (meaning: entry alr exist)
            #if none: havent exist.
            course=session.query(Course).filter(Course.udemy_url == item['udemy_url']).limit(1).with_for_update().one_or_none()
            if course is not None:
                item_dict=dict(item)
                for key, value in item_dict.items():
                    setattr(course,key,value)
                session.add(course)
                session.commit()
            else:
                course = Course(**item)
                session.add(course)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
