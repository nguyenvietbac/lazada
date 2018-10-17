# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pymongo
import datetime

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["admin"]
# mycol = mydb["Price"]

class AutoSpider(CrawlSpider):
    download_delay = 0.2
    download_timeout = 30
    # DUPEFILER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
    name = 'vuivui'
    allowed_domains = ["vuivui.com"]
    start_urls = ['https://www.vuivui.com/']

    # root layer
    def parse(self, response):
        # links = response.xpath('//div[@class="wrap"]/a/@href').extract()

        tab = []
    #     tab.append(links[0])
    #     request = scrapy.Request(response.urljoin(links[0]), callback=self.parse_htd)
    #     # request.meta['item'] = links
    #     request.meta['tab'] = tab
    #     yield request
            
    # # hang tieu dung layer 1
    # def parse_htd(self, response):
    #     # take = response.meta['item']
    #     tab = response.meta['tab']
    #     #check this layer
        links = response.xpath('//div[@id="mainctnr"]/div/div/a/@href').extract()
        if links == []:
            links = response.xpath('//div[@class="fitem"]/a/@href').extract()
        count = 0
        for link in links:
            if link.find('?') == -1:
                temp_tab = []
                temp_tab.append(link)
                request = scrapy.Request(response.urljoin(link), callback=self.parse_htd1)
                request.meta['tab'] = temp_tab + tab
                # request.meta['item'] = take + links
                yield request
                count = count + 1
        # yield{
        #     'data' : links
        # }
    # hang tieu dung layer 2
    def parse_htd1(self, response):
        # take = response.meta['item']
        tab = response.meta['tab']
        links = response.xpath('//ul[@class="catemenus"]/li/a/@href').extract()
        
        # count = 0
        if links == []:
            request = scrapy.Request(response.urljoin(response.url), dont_filter = True, callback=self.parse_check_htd)
            request.meta['tab'] = tab
            # request.meta['item'] = take + links
            yield request            
        else:
            for link in links:
                if link.find('?') == -1:
                    temp_tab = []
                    temp_tab.append(link)
                    request = scrapy.Request(response.urljoin(link), callback=self.parse_htd2)
                    request.meta['tab'] = temp_tab + tab
                    # request.meta['item'] = take + links
                    yield request

    def parse_htd2(self, response):
        # take = response.meta['item']
        tab = response.meta['tab']
        links = response.xpath('//ul[@class="catemenus"]/li/a/@href').extract()
        
        if links == []:
            request = scrapy.Request(response.urljoin(response.url), dont_filter = True, callback=self.parse_check_htd)
            request.meta['tab'] = tab
            # request.meta['item'] = take + links
            yield request            
        else:
            for link in links:
                if link.find('?') == -1:
                    temp_tab = []
                    temp_tab.append(link)
                    request = scrapy.Request(response.urljoin(link), callback=self.parse_check_htd)
                    request.meta['tab'] = temp_tab + tab
                    # request.meta['item'] = take + links
                    yield request


    # # hang tieu dung last and check layer
    def parse_check_htd(self, response):

        # take = response.meta['item']
        tab = response.meta['tab']
        le = len(tab)
        for x in range(0, le):
            tab[x] = tab[x].replace("/", "")
            tab[x] = tab[x].replace("-", " ")

        item = response.xpath('//*[@id="grid-product"]').extract()
        if item != []:
            name = response.xpath('//div[@id="grid-product"]/div/div[1]/text()').extract()
            price = response.xpath('//div[@id="grid-product"]/div/div/div[1]/text()').extract()

            if name == []:
                name = response.xpath('//div[@id="grid-product"]/div//div[@class="itemname"]/text()').extract()
            if price == []:
                price = response.xpath('//div[@id="grid-product"]//*[@class="detail"]/b/text()').extract()

            if name == []:
                name = response.xpath('//div[@id="grid-product"]/div//div[@class="riki-name"]/text()').extract() 
            if price == []:
                price = response.xpath('//div[@id="grid-product"]/div//div[@class="pricenew"]/text()').extract() 

            if len(name) == len(price):
                for x in range(0,len(name)):
                    temp_tab = []
                    tab_here = response.xpath('//div[@id="grid-product"]/div[$o]/div/span/a/text()',o = x + 1).extract()
                    producer = response.xpath('//div[@id="grid-product"]//div[$o]/div[2]/div/a/@title',o = x + 1).extract()
                    if producer == []:
                        producer = response.xpath('//div[@id="grid-product"]/div[$o]//a/@title',o = x + 1).extract()

                    temp_tab.append(tab_here)
                    price[x] = price[x].replace("\u20ab", "")
                    price[x] = price[x].replace(".", "")
                    # price[x] = int(price[x])
                    date = datetime.datetime.now().date()
                    date = str(date)
                    yield{
                        'properties' : tab_here + tab + producer,
                        'name' : name[x],
                        'price' : price[x],
                        'time' : date,
                        'source' : 'vuivui.com',
                        # 'pr' : producer,
                        # 'tab_here' : tab_here,
                    }

                    dic = {
                        'properties' : tab_here + tab + producer,
                        'name' : name[x],
                        'price' : price[x],
                        'time' : date,
                        'source' : 'vuivui.com',
                        # 'pr' : producer,
                        # 'tab_here' : tab_here,
                    }

                    # insert = mycol.insert_one(dic)

                    next_page = response.xpath('//a[@id="page-next"]/@href').extract() 
                    if next_page != []:
                        link = response.url
                        page = 2
                        link_out = link + '?page=' + str(1)
                        request = scrapy.Request(response.urljoin(link_out), callback=self.parse_next)
                        request.meta['link'] = link
                        request.meta['page'] = page
                        request.meta['tab'] = tab
                        # request.meta['item'] = take
                        yield request

    def parse_next(self, response):
        # take = response.meta['item']
        tab = response.meta['tab']
        le = len(tab)

        item = response.xpath('//*[@id="grid-product"]').extract()
        if item != []:
            name = response.xpath('//div[@id="grid-product"]/div/div[1]/text()').extract()
            price = response.xpath('//div[@id="grid-product"]/div/div/div[1]/text()').extract()

            if name == []:
                name = response.xpath('//div[@id="grid-product"]/div//div[@class="itemname"]/text()').extract()
            if price == []:
                price = response.xpath('//div[@id="grid-product"]//*[@class="detail"]/b/text()').extract()

            if name == []:
                name = response.xpath('//div[@id="grid-product"]/div//div[@class="riki-name"]/text()').extract() 
            if price == []:
                price = response.xpath('//div[@id="grid-product"]/div//div[@class="pricenew"]/text()').extract() 

            if len(name) == len(price):
                for x in range(0,len(name)):
                    temp_tab = []
                    tab_here = response.xpath('//div[@id="grid-product"]/div[$o]/div/span/a/text()',o = x + 1).extract()
                    producer = response.xpath('//div[@id="grid-product"]//div[$o]/div[2]/div/a/@title',o = x + 1).extract()
                    if producer == []:
                        producer = response.xpath('//div[@id="grid-product"]/div[$o]//a/@title',o = x + 1).extract()

                    temp_tab.append(tab_here)
                    price[x] = price[x].replace("\u20ab", "")
                    price[x] = price[x].replace(".", "")
                    # price[x] = int(price[x])
                    date = datetime.datetime.now().date()
                    date = str(date)
                    yield{
                        'properties' : tab_here + tab + producer,
                        'name' : name[x],
                        'price' : price[x],
                        'time' : date,
                        'source' : 'vuivui.com',
                        # 'pr' : producer,
                        # 'tab_here' : tab_here,
                    }

                    dic = {
                        'properties' : tab_here + tab + producer,
                        'name' : name[x],
                        'price' : price[x],
                        'time' : date,
                        'source' : 'vuivui.com',
                        # 'pr' : producer,
                        # 'tab_here' : tab_here,
                    }

                    # insert = mycol.insert_one(dic)

                    next_page = response.xpath('//a[@id="page-next"]/@href').extract() 
                    if next_page != []:
                        link = response.meta['link']
                        link_out = link + '?page=' + str(response.meta['page'])
                        request = scrapy.Request(response.urljoin(link_out), callback=self.parse_next)
                        request.meta['link'] = link
                        request.meta['page'] = response.meta['page'] + 1
                        request.meta['tab'] = tab
                        # request.meta['item'] = take
                        yield request
