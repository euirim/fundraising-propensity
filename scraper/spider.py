import datetime
from scrapy.spiders import SitemapSpider

class GoFundMeSitemapSpider(SitemapSpider):
    name = 'gofundme_sitemap_spider'
    allowed_domains = ['gofundme.com']
    sitemap_urls = ['https://www.gofundme.com/sitemap.xml']
    sitemap_rules = [
        ('/f/', 'parse_f'),
    ]
    download_delay = 0.5  # ms
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
    }

    def parse_f(self, response):
        print(response)
        pass

    def sitemap_filter(self, entries):
        # no filter at present
        for entry in entries:
            print(entry)
            yield entry