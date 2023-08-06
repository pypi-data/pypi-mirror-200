import scrapy


class MADSpider(scrapy.Spider):
    name = "mad2023"
    start_urls = ['https://mad.firstmark.com/card']

    def parse(self, response):

        for cie in response.xpath('/html/body/div/main/div/ul/li/h2/following-sibling::ul/li/ul/li'):
            yield {
                'category': cie.xpath('parent::ul/parent::li/parent::ul/parent::li/h2/text()').get(),
                'subcategory': cie.xpath('parent::ul/parent::li/h3/text()').get(),
                'name': cie.xpath('div/div/h2/text()').get(),
                'location': cie.xpath('div/div/span/text()').get(),
                'year': cie.xpath('div[2]/span/text()').get(),
                'funding': cie.xpath('div[2]/span[2]/text()').get(),
                'website': cie.xpath('a/text()').get(),
                'summary': cie.xpath('p/text()').get(),
            }
