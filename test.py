#
# items.py
#
import scrapy
from scrapy import Item, Field

class RunnerItem(Item):
    color = Field()
    size_width_list = Field()
    pass

#
# runner_spider.py
#

from scrapy.contrib.spiders import CrawlSpider
from selenium import webdriver
# from runner.items import RunnerItem

class RunnerSpider(CrawlSpider):
    name = 'test'
    allowed_domains = ['lazada.vn']
    start_urls = ['https://www.lazada.vn/chuot/']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        items = []
        self.driver.get(response.url)

        # get colors
        price = self.driver.find_elements_by_xpath('//div[@class="c13VH6"]/text()')
        # for color in color_tags:
        #     item = RunnerItem()
        #     color.click()
        #     color_str = self.driver.find_element_by_id('ref2QIColorTitle').text
        #     item['color'] = color_str

        #     #get sizes
        #     size_width_list = []
        #     size_tags = self.driver.find_elements_by_class_name('ref2QISize')
        #     for size in size_tags:
        #         size.click()
        #         size_str = size.get_attribute('name')

        #         #get widths
        #         width_tags = self.driver.find_elements_by_class_name('ref2QIWidth')
        #         for width in width_tags:
        #             width.click()
        #             width_str = width.get_attribute('name')
        #             availability_tag = self.driver.find_element_by_id('ref2QIInventoryTitleS')
        #             size_width_list.append([size_str, width_str, availability_tag.text])

        #     item['size_width_list'] = size_width_list
        #     items.append(item)
        yield{
            'price' : price
        }

        self.driver.close()
        return items
