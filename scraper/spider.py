import arrow
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
        # url
        url = response.url

        # title
        title = response.css('.a-campaign-title::text').get()

        # story
        story = response.css('.o-campaign-story p::text').extract()
        if len(story) == 0:
            story = response.css('.o-campaign-story::text').extract()
        story = ' '.join(story).replace('\xa0', ' ').replace('&nbsp;', ' ')

        # created
        created = response.css(
            '.m-campaign-byline-created::text'
        ).get().replace('Created ', '')
        created = arrow.get(created, 'MMMM D, YYYY').date()

        # raised
        finances = response.css('.m-progress-meter-heading')
        raised = finances.css('::text').get()
        raised = int(raised.replace('$', '').replace(',', ''))

        # goal
        text_stat = finances.css('.text-stat::text').get().split()
        finished = False
        goal = None
        if text_stat[-1].strip() == 'raised':
            finished = True
        else:
            goal = finances.css('.text-stat::text').get().split()[-2]
            goal = int(goal.replace('$', '').replace(',', ''))

        # category
        category = response.css('.m-campaign-byline-type::text').get()

        # first cover image
        cover_image_style = response.css('div.a-image').get()
        first_cover_image = cover_image_style[
            cover_image_style.find("(")+1:cover_image_style.find(")")
        ]

        # story images
        story_images = response.css('.o-campaign-story img::attr(src)').extract()

        yield {
            'url': url,
            'title': title,
            'story': story,
            'created': created,
            'raised': raised,
            'goal': goal,
            'category': category,
            'finished': int(finished),
            'first_cover_image': first_cover_image,
            'story_images': story_images,
        }

    def sitemap_filter(self, entries):
        # no filter at present
        for entry in entries:
            yield entry