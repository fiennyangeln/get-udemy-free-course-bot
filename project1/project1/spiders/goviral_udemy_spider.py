import scrapy
from project1.items import UrlItem

class GoViralUdemySpider(scrapy.Spider):
    name = "goviral-udemy"
    start_urls = [
        'https://udemycoupon.learnviral.com/coupon-category/free100-discount/',
    ]


    def parse(self, response):
        for wholeBox in response.css('div.item-holder'):
            item=UrlItem()
            name=wholeBox.css('a::attr(title)').extract_first()
            title=name.split('"')[1]
            item['course_name']='"%s"' % (title)
            item['udemy_url']=wholeBox.css('div.item-actions a::attr(href)').extract_first().split('\n')[0]
            yield item

        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
