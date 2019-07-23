import scrapy


class HohoyogaItem(scrapy.Item):
    pk = scrapy.Field()
    email = scrapy.Field()
    name = scrapy.Field()
    phone = scrapy.Field()
    location = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    until_at = scrapy.Field()
