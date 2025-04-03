import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class KsuSpiderSpider(CrawlSpider):
    name = 'ksu_spider'
    allowed_domains = ['www.kennesaw.edu']
    start_urls = ['https://www.kennesaw.edu/']

    rules = (
        Rule(LinkExtractor(allow_domains=['kennesaw.edu']), callback='parse_item', follow=True),
    )

    custom_settings = {
        'USER_AGENT': 'KSU CS4422-IRbot/0.1',
        'DOWNLOAD_DELAY': 1.0,
        'CLOSESPIDER_PAGECOUNT': 1000,  # Terminate after collecting 1000 pages
        'ROBOTSTXT_OBEY': False,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'ksu1000.json',  # Save data to JSON file
    }

    def parse_item(self, response):
        # Extract and process the necessary information
        entry = {
            'pageid': response.url,  # You can use the URL as a unique identifier
            'url': response.url,
            'title': response.xpath('//title/text()').get(),
            'body': ' '.join(response.css('p::text').getall()),  # Extract text from paragraphs
            'emails': [],  # You will populate this list with emails
        }

        # Extract emails using regular expressions
        entry['emails'] = re.findall(r'\S+@\S+', entry['body'])

        yield entry
