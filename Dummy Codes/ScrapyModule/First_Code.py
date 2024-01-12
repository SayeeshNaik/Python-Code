import scrapy

class quotespider(scrapy.Spider):
    name = "extractor"
    
    def start_requests(self):
        urls = ['http://quotes.toscrape.com/page/1/']
        
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    
    def parse(self,response):
        page = response.url.split("/")[-2]
        filename = "quotes.html"
        
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('Saved file ',filename)