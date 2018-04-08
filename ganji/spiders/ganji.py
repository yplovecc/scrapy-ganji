# -*- coding: UTF-8 -*-
from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import scrapy
from ganji.items import GanjiItem
import pymongo

class ganji(scrapy.Spider):
    name = "ganji"
    start_urls = [
                'http://wh.ganji.com/danbaobaoxian/o1/',
                ]
    http = 'http://'
    domain = 'wh.ganji.com'

    def parse(self, response):
        self.logger.info('Parse url %s' % response.url)
        suburls = response.selector.xpath("//a[contains(@class,'list-info-title')]/@href").extract()
        
        for suburl in suburls:
            suburl = suburl.lstrip('//%s'%self.domain)
            suburl = self.http + self.domain + '/' + suburl + 'contactus/#tabl'
            yield scrapy.Request(suburl, callback=self.parse_item)
        next_url = response.xpath("//ul[@class='pageLink clearfix']/li[last()]/a/@href").extract_first()
        if next_url:
            next_url = self.http + self.domain + next_url
            time.sleep(5)
            yield scrapy.Request(next_url)

    def parse_item(self, response):
        self.logger.info('Parse suburl %s' % response.url)
        contacts= response.selector.xpath("//div[@id='dzcontactus']")
        if len(contacts) == 0:return
        item = GanjiItem()
        contact = contacts[0]
        xname = u"//span[text()='联 系 人：' and @class='t']/following-sibling::p[1]/text()"
        item['name'] = contact.xpath(xname).extract_first().strip().strip('\n') if len(contact.xpath(xname)) != 0 else ''

        xe164 = u"//span[text()='联系电话：' and @class='t']/following-sibling::p[1]/text()"
        item['e164'] = contact.xpath(xe164).extract_first().strip().strip('\n') if len(contact.xpath(xe164)) != 0 else ''

        xcompany = u"//span[text()='公司名称：' and @class='t']/following-sibling::div[1]/h1/text()"
        item['company'] = contact.xpath(xcompany).extract_first().strip().strip('\n') if len(contact.xpath(xcompany)) != 0 else ''

        item['source'] = 'ganji'
        item['url'] = response.url
        item['content'] = contact.xpath(u"//li[@class='fb']/text()").extract_first().strip().strip('\n') 
        item['insertime'] = int(time.time())
        yield item




