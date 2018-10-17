# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pymongo
import datetime
import json

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["admin"]
# mycol = mydb["Price"]

class AutoSpider(CrawlSpider):
    download_delay = 0.2
    download_timeout = 30
    name = 'tiki'
    allowed_domains = ["tiki.vn"]
    start_urls = ['https://tiki.vn/']

    #root layer
    def parse(self, response):

        tab1 = response.xpath('//div[@class="main-nav"]//ul/li/a/span[2]/text()').extract()
        for x in range(len(tab1)):
            tab2 = response.xpath('//div[@class="main-nav"]//ul/li[$o]/div/ul/li/div/a[@class=""]/text()', o = x + 1).extract()
            links = response.xpath('//div[@class="main-nav"]//ul/li[$o]/div/ul/li/div/a[@class=""]/@href', o = x + 1).extract()
            if x == 0:
                addition_tab2 = response.xpath('//div[@class="main-nav"]//ul/li[1]/div/ul/li[3]/div/a[@class="bold "]/text()').extract()
                addition_links = response.xpath('//div[@class="main-nav"]//ul/li[1]/div/ul/li[3]/div/a[@class="bold "]/@href').extract()
                tab2 = tab2 + addition_tab2
                links = links + addition_links
                # yield{
                #     'test' : tab2,
                #     'links' : links
                # }
            
            for y in range(len(links)):
                request = scrapy.Request(response.urljoin(links[y]), callback=self.parse_check)
                temp = []
                temp.append(tab1[x])
                temp.append(tab2[y])
                tab = temp
                request.meta['tab'] = tab
                yield request

    def parse_check(self, response):
        tab = response.meta['tab']

        name = response.xpath('//div[@class="product-box-list"]//div/a[@class=""]/@title').extract()
        price = response.xpath('//div[@class="product-box-list"]/div//span[@class="final-price"]/text()').extract()

        for x in range(len(name)):
            date = datetime.datetime.now().date()
            date = str(date)
            price[x] = price[x].replace("\u00a0\u20ab", "")
            tab[1] = tab[1].replace("\n                                                    ","")
            tab[1] = tab[1].replace("                                                ","")
            yield{
                'name' : name[x],
                'price' : price[x],
                'properties' : tab,
                'time' : date,
                'source' : 'tiki.vn'
            }


        next_page = response.xpath('//a[@class="next"]').extract()
        if next_page != []:
            link = response.url
            page = 2
            link_out = link + '&page=' + str(1)
            request = scrapy.Request(response.urljoin(link_out), callback=self.parse_next)
            request.meta['link'] = link
            request.meta['page'] = page
            request.meta['tab'] = tab
            yield request


    def parse_next(self, response):
        tab = response.meta['tab']
        link = response.meta['link']
        page = response.meta['page']

        name = response.xpath('//div[@class="product-box-list"]//div/a[@class=""]/@title').extract()
        price = response.xpath('//div[@class="product-box-list"]/div//span[@class="final-price"]/text()').extract()

        for x in range(len(name)):
            date = datetime.datetime.now().date()
            date = str(date)
            price[x] = price[x].replace("\u00a0\u20ab", "")
            tab[1] = tab[1].replace("\n                                                    ","")
            tab[1] = tab[1].replace("                                                ","")
            yield{
                'name' : name[x],
                'price' : price[x],
                'properties' : tab,
                'time' : date,
                'source' : 'tiki.vn' 
            }


        next_page = response.xpath('//a[@class="next"]').extract()
        if next_page != []:
            link_out = link + '&page=' + str(page)
            request = scrapy.Request(response.urljoin(link_out), callback=self.parse_next)
            request.meta['link'] = link
            request.meta['page'] = page + 1
            request.meta['tab'] = tab
            yield request
        # if name == [] and price == []:
        #     yield{
        #         'tab' : tab
        #     }

# class TikiPipeline(object):
#     """docstring for WriteJson"""
#     def open_spider(self, spiders):
#         self.file = open('test.json', 'w')
    
#     def close_spider(self, spiders):
#         self.file.close()
        
#     def process_item(self, item, spiders):
#         line = json.dump(dict(item)) + "\n"
#         self.file.write(line)
#         return item