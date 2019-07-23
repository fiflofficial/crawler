from scrapy.exceptions import DropItem


class ValidatesPipeline(object):
    def process_item(self, item, spider):
        name = item.get('name')
        email = item.get('email')
        if not email:
            raise DropItem("Useless item founded")
        return item


class DuplicatesPipeline(object):
    __slots__ = ['seen']
    
    def __init__(self):
        self.seen = set()
    
    def process_item(self, item, spider):
        if item['email'] in self.seen:
            raise DropItem("Duplicate item founded")

        self.seen.add(item['email'])
        return item
