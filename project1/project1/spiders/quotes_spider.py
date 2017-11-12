import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.goodreads.com/quotes/tag/books',
    ]

    
    def parse(self, response):
        page=response.url.split("/")[-1].split("=")[-1]
        filename ='quotes-%s.txt' % page
        enc ='utf-8'
        f=open(filename,'a',encoding=enc)
        f.write(response.url)
        for quote in response.css('div div.quoteText'):
            text=quote.css('::text').extract_first()
            #print(text)
            f.write(text)

        next_page = response.css('div a.next_page::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
