import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pymongo
import datetime

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["Dulieu_adaroi"]
# mycol = mydb["Price"]

class AutoSpider(CrawlSpider):
    download_delay = 0.1
    download_timeout = 30
    name = 'ada1'
    allowed_domains = ["adayroi.com"]
    start_urls = ['https://www.adayroi.com']
    def parse(self, response):
        tab1 = response.xpath('//li[@class="menu__cat-item"]/a/text()').extract()
        tab2 = []
        tab = []
        print(tab1[1])
        for x in range(len(tab1)):
            if x == 0:
                continue
            temp = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*', o = x +1).extract()
            for y in range(len(temp)):
                temp2 = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*[$p]/@class', o = x + 1, p = y + 1).extract()
                if temp2 == ['item-strong']:
                    tab2 = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*[$p]/text()', o = x + 1, p = y + 1).extract()
                    if tab2 == ['Tất cả danh mục']:
                        continue
                    next_line = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*[$p]/li[1]', o = x +1, p = y + 2).extract()
                    # if next_line == []:
                    link = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*[$p]/@href', o = x + 1, p = y + 1).extract()
                    if link != []:
                        request = scrapy.Request(response.urljoin(link[0]), callback=self.parse_last)
                        temp = []
                        temp.append(tab1[x])
                        tab = tab2 + temp
                        # print(tab)
                        request.meta['tab'] = tab
                        yield request

                small = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*[$p]/li[1]', o = x +1, p = y + 1).extract()
                if small != []:
                    links = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*[$p]/li/a/@href', o = x +1, p = y + 1).extract()
                    tab3 = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*[$p]/li/a/text()', o = x +1, p = y + 1).extract()
                    if len(links) == len(tab3):
                        for z in range(len(links)):
                            request = scrapy.Request(response.urljoin(links[z]), callback=self.parse_last)      
                            tab2 = response.xpath('//li[@class="menu__cat-item"][$o]/div[@class="menu__cat-list menu__cat-list--child"]/*[$p]/text()', o = x + 1, p = y ).extract()
                            temp = []
                            temp.append(tab1[x])
                            temp.append(tab3[z])
                            tab = tab2 + temp
                            request.meta['tab'] = tab
                            # yield request
                            # yield{
                            #   'tab1' : tab,
                            #   'tab2' : links[z],
                            #   # 'link' p: link
                            # }
    def parse_last(self, response):
        tab = response.meta['tab']      
        names = response.xpath('//*[@class="product-item__info-title"]/text()').extract()
        prices = response.xpath('//*[@class="product-item__info-price"]/span[1]/text()').extract()

        if len(names) == len(prices):
            for x in range(len(names)):
                date = datetime.datetime.now().date()
                date = str(date)
                prices[x] = prices[x].replace(".", "")
                prices[x] = prices[x].replace("\u0111", "")
                yield{
                    'name' : names[x],
                    'price' : prices[x],
                    'properties' : tab,
                    'date' : date,
                    'source' : 'adayroi.com',
                }
                dic = {
                    'name' : names[x],
                    'price' : prices[x],
                    'properties' : tab,
                    'date' : date,
                    'source' : 'adayroi.com',   
                }

                # insert = mycol.insert_one(dic)

        next_page = response.xpath('//a[@aria-label="Next"]').extract()
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
        names = response.xpath('//*[@class="product-item__info-title"]/text()').extract()
        prices = response.xpath('//*[@class="product-item__info-price"]/span[1]/text()').extract()

        if len(names) == len(prices):
            for x in range(len(names)):
                date = datetime.datetime.now().date()
                date = str(date)
                prices[x] = prices[x].replace(".", "")
                prices[x] = prices[x].replace("\u0111", "")
                yield{
                    'name' : names[x],
                    'price' : prices[x],
                    'properties' : tab,
                    'date' : date,
                    'source' : 'adayroi.com',
                }
                dic = {
                    'name' : names[x],
                    'price' : prices[x],
                    'properties' : tab,
                    'date' : date,
                    'source' : 'adayroi.com',   
                }

                # insert = mycol.insert_one(dic)

        next_page = response.xpath('//a[@aria-label="Next"]').extract()
        if next_page != []:
            link_out = link + '&page=' + str(page)
            request = scrapy.Request(response.urljoin(link_out), callback=self.parse_next)
            request.meta['link'] = link
            request.meta['page'] = page + 1
            request.meta['tab'] = tab
            yield request

            