import scrapy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project1.items import CourseItem, Course
import datetime
import re

now = datetime.datetime.now()
date_last_checked = datetime.datetime(now.year, now.month, now.day)

def get_next_url():
    engine = create_engine('sqlite:///courses.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    allList=session.query(Course).filter(Course.checkout_url.is_(None))
    session.close()
    for item in allList:
        yield item.udemy_url

class udemyAddInfoSpider(scrapy.Spider):
    name = "udemy-addinfo"
    start_urls = []
    allowed_domains = ["udemy.com"]
    url=get_next_url()
    def start_requests(self):
        yield self.make_requests_from_url(next(self.url))


    def parse(self, response):
        item = CourseItem()
        item['udemy_url']=response.url

        item['course_name'] = response.css('h1.clp-lead__title::text').extract_first().strip()
        checkout_url = response.css('a.course-cta--buy::attr(href)').extract_first()

        if (checkout_url is not None):
            checkout_url = "https://www.udemy.com" + checkout_url
            item['checkout_url']=checkout_url

        price = response.css('span.price-text__current')
        if (price is None or price.css('span.sr-only::text').extract_first() is None):
            yield item
        else:
            tagline=price.css('span.sr-only::text').extract_first()
            if ("Current price" in tagline):
                discounted_price=price.css('::text').extract()[-1]
                if ("Free" in discounted_price):
                    discounted_price=0
                else:
                    discounted_price=int(re.findall('\d+', discounted_price)[0])
                item['discounted_price'] = discounted_price
                ori = response.css("span.price-text__old--price::text").extract()
                original_price = ori[1].split("\n")[0].strip()
                original_price = int(re.findall('\d+', original_price)[0])
                item['original_price']=original_price
            elif ("Price" in tagline):
                price=price.css('::text').extract()[-1]
                if ("Free" in price):
                    price=0
                else:
                    price=int(re.findall('\d+', price)[0])
                item['discounted_price']=item['original_price']=price
        yield item

        next_page = next(self.url)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next(self.url))
