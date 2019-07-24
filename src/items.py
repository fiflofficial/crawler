import scrapy


class HohoyogaItem(scrapy.Item):
    email = scrapy.Field()
    name = scrapy.Field()
    phone = scrapy.Field()
    location = scrapy.Field()
    type = scrapy.Field()
    path = scrapy.Field()
