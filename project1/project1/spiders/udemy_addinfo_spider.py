import scrapy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project1.items import CourseItem, Course
import datetime
import re

now = datetime.datetime.now()
date_last_checked = datetime.datetime(now.year, now.month, now.day)

#get the udemyURL which has not have checkoutURL
def get_next_url():
    engine = create_engine('sqlite:///courses.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    allList=session.query(Course).filter(Course.checkout_url.is_(None))
    session.close()
    for item in allList:
        yield item.udemy_url

#this spider is meant for adding checkout url, currentprice, originalprice to the DB
#for every udemyURL in DB that hasnt been updated
class udemyAddInfoSpider(scrapy.Spider):
    name = "udemy-addinfo"
    start_urls = []
    allowed_domains = ["udemy.com"]
    url=get_next_url()

    #to initiate the request
    def start_requests(self):
        yield self.make_requests_from_url(next(self.url))


    def parse(self, response):
        item = CourseItem()
        #get the url we r now in
        item['udemy_url']=response.url

        #get the checkout URL, if there is any
        item['course_name'] = response.css('h1.clp-lead__title::text').extract_first().strip()
        checkout_url = response.css('a.course-cta--buy::attr(href)').extract_first()
        if (checkout_url is not None):
            checkout_url = "https://www.udemy.com" + checkout_url
            item['checkout_url']=checkout_url

        #get the ori price and current price, if there is any
        price = response.css('span.price-text__current')
        #if the course is no longer available for purchase/enroll
        if (price is None or price.css('span.sr-only::text').extract_first() is None):
            yield item
        else:
            tagline=price.css('span.sr-only::text').extract_first()
            #if there is currentprice, it means there is discount.
            #NOT NECESSARILY FREE THO HAHAHAHAHAHAHAHAHHA OMG UNTUNG BELOM BELI YANG BAYAR OMG OMG
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
            #this one means no discount.
            #NOT NECESSARILY PAID, there are courses that is free dari dulu
            elif ("Price" in tagline):
                price=price.css('::text').extract()[-1]
                if ("Free" in price):
                    price=0
                else:
                    price=int(re.findall('\d+', price)[0])
                item['discounted_price']=item['original_price']=price
        yield item

        #get the next page url from DB
        next_page = next(self.url)
        if next_page is not None:
            #TODO: INI PERLU URLJOIN GK YA HMMMM
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next(self.url))
