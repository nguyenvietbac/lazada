# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pymongo
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Dulieu_lazada"]
mycol = mydb["Price"]

class AutoSpider(CrawlSpider):
    download_delay = 0.2
    download_timeout = 30
    name = 'laz1'
    allowed_domains = ["lazada.vn"]
    start_urls = ['https://www.lazada.vn/']
    def parse(self, response):
        tabs1 = response.xpath('//ul[@class="lzd-site-menu-root"]/li/a/span/text()').extract()

        for x in range(len(tabs1)):
            tabs2 = response.xpath('//ul[@class="lzd-site-menu-root"]/ul[$o]/li/a/span/text()', o = x + 1).extract()
            for y in range(len(tabs2)):
                links = response.xpath('//ul[@class="lzd-site-menu-root"]/ul[$o]/li[$a]/ul//@href', o = x + 1, a = y + 1).extract()
                if links == []:
                    links = response.xpath('//ul[@class="lzd-site-menu-root"]/ul[$o]/li[$a]/a//@href', o = x + 1, a = y + 1).extract()
                for link in links:
                    tab = []
                    ltab = link.replace("//www.lazada.vn/", "")
                    ltab = ltab.replace("/", "")
                    ltab = ltab.replace("-", " ")
                    tab.append(ltab)
                    tab.append(tabs1[x])
                    tab.append(tabs2[y])
                    request = scrapy.Request(response.urljoin(link), self.parse_laz1, meta={
                        'splash': {
                            'endpoint': 'render.html',
                            'args': {'wait': 0.5}
                        }
                    })
                    request.meta['tab'] = tab
                    request.meta['item'] = link
                    yield request
            #         break
            #     break
            # break

    def parse_laz1(self, response):
        link_prev = response.meta['item']
        tab = response.meta['tab']
        names = response.xpath('//div[@class="c16H9d"]/a/@title').extract()
        prices = response.xpath('//div[@class="c3gUW0"]/span/text()').extract()

        for x in range(len(names)):
            prices[x] = prices[x].replace(".", "")
            prices[x] = prices[x].replace("\u20ab", "")
            prices[x] = prices[x].replace("\u00a0", "")
            date = datetime.datetime.now().date()
            date = str(date)
            yield{
                'names' : names[x],
                'prices' : prices[x],
                'propeties' : tab,
                'time' : date,
                'source' : 'lazada.vn',
            }        
            dic = {
                'names' : names[x],
                'prices' : prices[x],
                'propeties' : tab,
                'time' : date,
                'source' : 'lazada.vn',
            }

            insert = mycol.insert_one(dic)
        next_page = response.xpath('//li[@class=" ant-pagination-next"]').extract()
        # if next_page == []:
        #     next_page = response.xpath('//li[@class="ant-pagination-next"]').extract()
    
        if next_page != []:
            link = link_prev
            link_out = link + '?page=' + str(2)
            request = scrapy.Request(response.urljoin(link_out), self.parse_next, meta={
               'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })
            request.meta['tab'] = tab
            request.meta['item'] = link_prev 
            request.meta['page'] = 3
            yield request
 
    def parse_next(self, response):
        link_prev = response.meta['item']
        tab = response.meta['tab']
        page = response.meta['page']
        names = response.xpath('//div[@class="c16H9d"]/a/@title').extract()
        prices = response.xpath('//div[@class="c3gUW0"]/span/text()').extract()

        for x in range(len(names)):
            prices[x] = prices[x].replace(".", "")
            prices[x] = prices[x].replace("\u20ab", "")
            prices[x] = prices[x].replace("\u00a0", "")
            date = datetime.datetime.now().date()
            date = str(date)
            yield{
                'names' : names[x],
                'prices' : prices[x],
                'propeties' : tab,
                'time' : date,
                'source' : 'lazada.vn',
                'page' : page - 1
            }        
            dic = {
                'names' : names[x],
                'prices' : prices[x],
                'propeties' : tab,
                'time' : date,
                'source' : 'lazada.vn',
            }

            insert = mycol.insert_one(dic)
            next_page = response.xpath('//li[@class=" ant-pagination-next"]').extract()
            # if next_page == []:
            #     next_page = response.xpath('//li[@class="ant-pagination-next"]').extract()
        
            
            if next_page != []:
                link = link_prev 
                link_out = link + '?page=' + str(page)
                request = scrapy.Request(response.urljoin(link_out), self.parse_next, meta={
                    'splash': {
                        'endpoint': 'render.html',
                        'args': {'wait': 0.5}
                    }
                })
                request.meta['tab'] = tab
                request.meta['item'] = link_prev 
                request.meta['page'] = page + 1
                yield request
	 
            