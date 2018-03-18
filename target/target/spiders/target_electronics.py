# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from target.items import TargetItem

class TargetElectronicsSpider(CrawlSpider):
    name = 'target-electronics'
    allowed_domains = ['target.com']
    start_urls = ['https://redsky.target.com/v1/plp/search/?count=24&offset=48&category=5xtg6&visitorId=01602E03E8670201824D2E9549AE113C&pageId=%2Fc%2F5xtg6&channel=web']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.sc-eHgmQL.kiIEUa.sc-bZQynM.jWgpUn.sc-EHOje.eRgKqV',)),
             callback="parse_item",
             follow=False),)

    def parse_item(self, response):
        #item_links = response.xpath('//h3[contains(@class, ".sc-uJMKN.jpuBaC")]').extract()
        item_links = response.css('.h-display-block.sc-EHOje.eRgKqV::attr(href)').extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        title = response.css('span[itemprop="name"]::text').extract()[0].strip()
        price = response.css('div[data-test="product-price"] > h-text-xl.h-text-bold::text').extract()[0]

        item = TargetItem()
        item['title'] = title
        item['price'] = price
        item['url'] = response.url
        yield item
