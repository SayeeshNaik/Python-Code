import scrapy
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from scrapy.spiders import SitemapSpider
import pymongo
import html

class AjioPDP(scrapy.Spider):
    name = "ajiopdp"
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(options=options)
        
        
    def start_requests(self):
        url = "https://www.ajio.com/p/460453610_white"
        xpath = "//div[@class='main-view product-view false']"
        yield scrapy.Request(url,callback=self.parse)
        
    
    
    def parse(self,response):
        url = "https://www.ajio.com/p/460453610_white"
        self.driver.get(url)
        response.body = self.driver.page_source
        body_str = str(response.body, response._body_declared_encoding())
        unescaped_body = html.unescape(body_str)
        new_response = response.replace(body=unescaped_body)
        print("nnnnnnnnnnnn = ",new_response.body)
        self.driver.quit()