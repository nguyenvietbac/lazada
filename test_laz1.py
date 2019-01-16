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
	download_delay = 1.5
	download_timeout = 180
	name = 'tlaz1'
	allowed_domains = ["lazada.vn"]
	start_urls = ['https://www.lazada.vn/']
	def parse(self, response):
		tabs1 = response.xpath('//ul[@class="lzd-site-menu-root"]/li/a/span/text()').extract()


		for x in range(len(tabs1)):
			tabs1[x] = "1 " + tabs1[x]
			tabs2 = response.xpath('//ul[@class="lzd-site-menu-root"]/ul[$o]/li/a/span/text()', o = x + 1).extract()

			links = response.xpath('//ul[@class="lzd-site-menu-root"]/ul[$o]/li/a/@href', o = x + 1).extract()

			# print(tabs2)
			# print(links)
			for y in range(len(tabs2)):
				tabs2[y] = "2 " + tabs2[y]
				tab = []
				# ltab = link.replace("//www.lazada.vn/", "")
				# ltab = ltab.replace("/", "")
				# ltab = ltab.replace("-", " ")
				# tab.append(ltab)
				tab.append(tabs1[x])
				tab.append(tabs2[y])
				request = scrapy.Request(response.urljoin(links[y]), self.parse_laz1, meta={
					'splash': {
						'endpoint': 'render.html',
						'args': {'wait': 0.5}
					}
				})
				request.meta['tab'] = tab
				request.meta['item'] = links[y]
				yield request
				# print(tab)

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
				'name' : names[x],
				'price' : prices[x],
				'propeties' : tab,
				'time' : date,
				'source' : 'lazada.vn',
				'page' : '1'
			}        
			dic = {
				'name' : names[x],
				'price' : prices[x],
				'propeties' : tab,
				'time' : date,
				'source' : 'lazada.vn',
			}

			# insert = mycol.insert_one(dic)
		next_page = response.xpath('//li[@class=" ant-pagination-next"]').extract()
		# if next_page == []:
		#     next_page = response.xpath('//li[@class="ant-pagination-next"]').extract()
		# print(next_page)	
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
			print(1)
 
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
				'name' : names[x],
				'price' : prices[x],
				'propeties' : tab,
				'time' : date,
				'source' : 'lazada.vn',
				'page' : page - 1
			}        
			dic = {
				'name' : names[x],
				'price' : prices[x],
				'propeties' : tab,
				'time' : date,
				'source' : 'lazada.vn',
			}

			# insert = mycol.insert_one(dic)
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
