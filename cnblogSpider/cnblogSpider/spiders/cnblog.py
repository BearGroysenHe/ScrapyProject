# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append('..')
from items import CnblogspiderItem
from scrapy.selector import Selector

class CnblogSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://www.cnblogs.com/qiyeboy/default.html?page=1']

    def parse(self, response):
        papers = response.xpath(".//*[@class='day']")
        for paper in papers:
            url = paper.xpath(".//*[@class='postTitle']/a/@href").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/text()").extract()[0]
            time = paper.xpath(".//*[@class='dayTitle']/a/text()").extract()[0]
            content = paper.xpath(".//*[@class='postCon']/div/text()").extract()[0]
            item = CnblogspiderItem(url=url, time=time, title=title, content=content)
            yield item
        next_page = Selector(response).re('<a href="(\S)">下一页</a>')
        if next_page:
            yield scrapy.Request(url = next_page[0],callback=self.parse)