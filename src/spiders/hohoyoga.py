from scrapy.http import FormRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..loaders import HohoyogaLoader
from ..items import HohoyogaItem


class HohoyogaSpider(CrawlSpider):
    name = "hohoyoga"
    start_urls = ['https://www.hohoyoga.com/index.php?act=dispMemberLoginForm']
    allowed_domains = ['www.hohoyoga.com']
    allowed_links = (
        'job_pilates_seoul$', 'index.php\?mid=job_pilates_seoul&page=\d{1}(\d{1})?(\d{1})?$',
        'job_pilates_kyongin$', 'index.php\?mid=job_pilates_kyongin&page=\d{1}(\d{1})?(\d{1})?$',
        'job_pilates_other$', 'index.php\?mid=job_pilates_other&page=\d{1}(\d{1})?(\d{1})?$',
        'job_info$', 'index.php\?mid=job_info&page=\d{1}(\d{1})?$',
        'job_health$', 'index.php\?mid=job_health&page=\d{1}(\d{1})?$',
        'job_other$', 'index.php\?mid=job_other&page=\d{1}(\d{1})?$',
    )
    allowed_items = (
        'job_pilates_seoul/\d+$', 'job_pilates_seoul&page=\d+&document_srl=\d+$',
        'job_pilates_kyongin/\d+$', 'job_pilates_kyongin&page=\d+&document_srl=\d+$',
        'job_pilates_other/\d+$', 'job_pilates_other&page=\d+&document_srl=\d+$',
        'job_info/\d+$', 'job_info&page=\d+&document_srl=\d+$',
        'job_health/\d+$', 'job_health&page=\d+&document_srl=\d+$',
        'job_other/\d+$', 'job_other&page=\d+&document_srl=\d+$',
    )

    rules = (
        Rule(LinkExtractor(allow=allowed_links)),
        Rule(LinkExtractor(allow=allowed_items), callback='parse_item'),
    )

    def parse_start_url(self, response):
        return FormRequest.from_response(
            response,
            formdata={'user_id': '', 'password': ''},
            formxpath='//form',
        )

    def parse_item(self, response):
        l = HohoyogaLoader(item=HohoyogaItem(), response=response)
        content_header_table = l.nested_xpath('//div[has-class("rd_body")]//table')
        content_header_table.add_xpath('name', '//tr[th[contains(text(), "업체명")]]//td/text()')
        content_header_table.add_xpath('until_at', '//tr[th[contains(text(), "마감날짜")]]//td/text()')
        content_header_table.add_xpath('location', '//tr[th[contains(text(), "지역")]]//td/text()')
        content_header_table.add_xpath('type', '//tr[th[contains(text(), "특기")]]//td/text()')
        content_header_table.add_xpath('phone', '//tr[th[contains(text(), "연락처")]]//td/text()')
        content_header_table.add_xpath('email', '//tr[th[contains(text(), "이메일")]]//td/text()')

        parsed_url = response.url.split('document_srl=')
        if len(parsed_url) < 2:
            parsed_url = response.url.split('/')
        l.add_value('url', response.url.replace('https://www.hohoyoga.com/', ''))
        l.add_value('pk', parsed_url[-1])

        return l.load_item()