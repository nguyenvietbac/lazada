# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import pymongo

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["thoitrang1"]
# mycol = mydb["products"]

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
					request.meta['item'] = links
					yield request
					break
				break
			break

	# def parse_laz1(self, response):
	# 	take = response.meta['item']
	# 	tab = response.meta['tab']
	# 	url = response.url
	# 	request = scrapy.Request(url, self.parse_laz2, meta={
	# 	    'splash': {
	# 	        'endpoint': 'render.html',
	# 	        'args': {'wait': 0.5}
	# 	    }
	# 	})
	# 	request.meta['tab'] = tab
	# 	request.meta['item'] = take
	# 	yield request

	def parse_laz1(self, response):
		take = response.meta['item']
		tab = response.meta['tab']
		# links = response.xpath('//span[@class="c13VH6"]/text()').extract()
		links = response.xpath('//div[@class="c16H9d"]/a/@href').extract()
		for link in links:
			request = scrapy.Request(response.urljoin(link), self.parse_laz2, meta={
				'splash': {
				    'endpoint': 'render.html',
				    'args': {'wait': 0.5}
				}
			})
			request.meta['tab'] = tab
			request.meta['item'] = take
			yield request


	def parse_laz2(self, response):
		take = response.meta['item']
		tab = response.meta['tab']
		
		name = response.xpath('//h1[@class="pdp-product-title"]/text()').extract()
		price = response.xpath('//span[@class=" pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl"]/text()').extract()
		if name == [] or price == []:
			print(tab)
		yield{
			'name' : name,
			'price' : price,
			'propeties' : tab,
		}

