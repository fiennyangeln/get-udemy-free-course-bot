import scrapy


class Product(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
