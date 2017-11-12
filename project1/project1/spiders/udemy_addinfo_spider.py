import scrapy
import csv

class udemyAddInfoSpider(scrapy.Spider):
    name = "udemy_addinfo"
    start_urls = []
    allowed_domains = ["udemy.com"]

    def start_requests(self):
        file=open('urldata.csv','r',encoding='utf-8')
        file.readline()
        file.readline()
        for line in file:
            url=line.split(",")[-1].split('\n')[0]
            yield self.make_requests_from_url(url)
            file.readline()
        file.close()
    def parse(self, response):
        #page=response.url.split("/")[-1].split("=")[-1]
        #filename ='urls.txt'
        #enc ='utf-8'
        #f=open(filename,'a',encoding=enc)
        #f.write(response.url)
        #for wholeHtml in response.css('div.link-holder'):
        #    text=wholeHtml.css('a::attr(href)').extract_first()
            #print(text)
            #f.write(text)
        item = response.css('span.price-text__current::text').extract()
        price = item[-1].split("\n")[0]
        print (price)

        #next_page = response.css('a.next::attr(href)').extract_first()
        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    print(next_page)
        #    yield scrapy.Request(
