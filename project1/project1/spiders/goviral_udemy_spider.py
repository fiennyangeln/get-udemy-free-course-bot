import scrapy
from project1.items import CourseItem
import datetime
now = datetime.datetime.now()
date_last_checked = datetime.datetime(now.year, now.month, now.day)
#This class is meant for filling the database with udemy_url that is free/in discounted Price
#We get the URL from goviral

class GoViralUdemySpider(scrapy.Spider):
    name = "goviral-udemy"
    start_urls = [
        'https://udemycoupon.learnviral.com/coupon-category/free100-discount/',
    ]


    def parse(self, response):
        #get the whole box for all course displayed in the current page
        for wholeBox in response.css('div.item-holder'):
            item=CourseItem()
            name=wholeBox.css('a::attr(title)').extract_first()
            title=name.split('"')[1]
            #get the coursename, udemyurl, add date_last_checked
            #TODO : check date_last_checked on udemy_addinfo
            #we put "" to handle comma (for later if we use .csv as output)
            item['course_name']='"%s"' % (title)
            item['udemy_url']=wholeBox.css('div.item-actions a::attr(href)').extract_first().split('\n')[0]
            item['date_last_checked']=date_last_checked
            #send item to pipeline
            yield item

        #get the next page from goviral
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
