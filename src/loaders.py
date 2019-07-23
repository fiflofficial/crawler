from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity
from w3lib.html import remove_tags, replace_entities, replace_escape_chars


def replace_useless_chars(text, which_ones=('\xa0', '\t', '\r'), replace_by=''):
    for uc in which_ones:
        text = text.replace(uc, replace_by)
    return text


class HohoyogaLoader(ItemLoader):
    default_output_processor = TakeFirst()
    
    content_in = MapCompose(remove_tags, replace_entities, replace_useless_chars)
    comment_in = MapCompose(remove_tags, replace_entities, replace_useless_chars)
    
    content_out = Identity()
    comment_out = str
