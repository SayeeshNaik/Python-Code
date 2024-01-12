import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    product_id = ["TSHGBUHJHRH3JJHJ","SHTGKUX3VWQVBRZY"]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        # self.driver = webdriver.Chrome(options=options)
        
    def start_requests(self):
            
        # for p_id in self.product_id :
            main_url = "https://www.flipkart.com/x/p/k?pid=" 
            url = "https://1.rome.api.flipkart.com/api/4/location/update"
            yield scrapy.Request(url, callback=self.parse,args={'wait': 0.5, 'viewport': '1024x2480', 'timeout': 90, 'images': 0, 'resource_timeout': 10})
        


    def parse(self, response):
        print("uuuuuuuuuuuuuuuuuuu")
        print(response.url)
        print(response.body)
        
        
        
        # self.driver.get(response.url)
        # name = self.driver.find_element(By.XPATH,'//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span[2]').text
        # # if(self.product_id.index(response.meta['id'])==0):
        # self.driver.find_element(By.XPATH,'//*[@id="container"]/div/div[3]/div[1]/div[2]/div[4]/div[1]/div[1]/div/div[2]/input').send_keys('581355')
        # self.driver.find_element(By.XPATH,'//*[@id="container"]/div/div[3]/div[1]/div[2]/div[4]/div[1]/div[1]/div/div[2]/span').click()
        # ot = self.driver.find_element(By.XPATH,'//*[@id="container"]/div/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div/div/div/div[1]/ul/div/div').text
        # print("nnnnnnnnnnnnnnnnnn = ",name)
        # print(response.url)
        # print(ot)
        # self.driver.close()
        
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"FlipkartPinCode.csv": {'format': 'csv', 'overwrite': True}}
                                   })
process.crawl(ProductSpider)
process.start()
