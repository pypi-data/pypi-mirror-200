import scrapy
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from twisted.internet.error import DNSLookupError
from scrapy.loader import ItemLoader

from data_job_crawler.crawler.helpers.extract_links import extract_links_from_file
from data_job_crawler.crawler.items import OldJobsCrawlerItem

FILEPATH = Path(__file__).parent.parent / 'data' / 'unscanned_urls.txt'


class OldwttjSpider(scrapy.Spider):
    """
    Detects if a job offer is still open on WTTJ website.
    """

    name = "oldwttj"
    allowed_domains = ["www.welcometothejungle.com"]
    start_urls = [
        "https://www.welcometothejungle.com/fr/companies/multiverse/jobs/director-data-engineering-infrastructure_london"]

    def start_requests(self):
        links = extract_links_from_file(FILEPATH)
        for link in links:
            if 'datai' not in link:  # website is down
                yield scrapy.Request(link, self.parse)

    def parse(self, response):
        l = ItemLoader(item=OldJobsCrawlerItem(), response=response)

        try:
            if response.xpath("//title[text()='Erreur 404']").get():
                l.add_value('old_url', response.url)
                yield l.load_item()
        except DNSLookupError:
            print('DNSLookupError\n')
            l.add_value('old_url', response.url)
            yield l.load_item()


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "ROBOTSTXT_OBEY": False,
            "ITEM_PIPELINES": {
                "data_job_crawler.crawler.pipelines.OldJobsCrawlerPipeline": 300,
            },
            "AUTOTHROTTLE_ENABLED": True,
            "AUTOTHROTTLE_TARGET_CONCURRENCY": 1,
            "AUTOTHROTTLE_START_DELAY": 5,
            "AUTOTHROTTLE_MAX_DELAY": 60,
        }
    )
    process.crawl(OldwttjSpider)
    process.start()
