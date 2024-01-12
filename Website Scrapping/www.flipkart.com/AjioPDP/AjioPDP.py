# Module And Libraries Import Field
import scrapy as sp
import pandas as pd
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
import requests
from bs4 import BeautifulSoup



class MyntrapdpSpider(sp.Spider):
    name = "ajio"
 
    fromDate = "2023-01-02"
    toDate   = "2023-01-03" 
    def start_requests(self,fromDate,toDate):
        url = 'https://hckinfo.kerala.gov.in/digicourt/Casedetailssearch/Orderbyorderdate_ajax/'
        data = {
            'from_date': '{}'.format(fromDate),
            'to_date': '{}'.format(toDate),
            'order_type': '1',
            'case_type': '',
            'case_no': '',
            'case_year': '',
            'cnt': '',
            'page_cnt': '',
            'reportable': 'undefined'
        }
        response = requests.post(url, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination = soup.find(class_ ="pagination")
        pagination = BeautifulSoup(str(pagination), "html.parser").findAll("a")[-1]
        lastpageApi = pagination["href"].split("Orderbyorderdate_ajax/")[-1]
        print("Total Records = ",int(lastpageApi)+20)
        looping = round(int(lastpageApi)/20) + 1
        main_df = pd.DataFrame(columns=["Sl No.","Case Details","Party Details","Order Details","PDF links"])
        
        apiNum = 0
        for page in range(looping):
            try: 
                temp_df = self.scrapper(data,apiNum)
                main_df = pd.concat([main_df, temp_df])
                main_df.to_excel("TableData ({} to {}).xlsx".format(self.from_date,self.to_date))
                print("Scrapped Records = ",apiNum+20,"({})".format(int(lastpageApi)+20))
                yield sp.Request(url, callback=self.scrapper,meta={"data":data,"apiNum":apiNum})
                apiNum += 20
            except: pass
        
        
    def pdfExtractor(token,lookups,citationno):
        pdfURL = '''https://hckinfo.kerala.gov.in/digicourt/Casedetailssearch/fileviewcitation?token={}&lookups={}&citationno={}'''.format(token,lookups, citationno)
        pdfURL = pdfURL.replace("'","")
        return pdfURL

    def scrapper(data,apiNum,self):
        url = 'https://hckinfo.kerala.gov.in/digicourt/Casedetailssearch/Orderbyorderdate_ajax/{}'.format(apiNum)
        response = requests.post(url, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        tableHTML = soup.find("table")
        pdfLinks = soup.findAll(class_ = "label label-info label-white middle")
        
        pdfLinks_list = []
        for pdfLink in pdfLinks:
            link = BeautifulSoup(str(pdfLink), 'html.parser')
            link = link.find("a")
            link = link["onclick"].split("viewordercitation(")[1:][0][0:-2].split(",")
            token = link[0]
            lookups = link[1]
            citationno  = link[2]
            final_pdf_link = self.pdfExtractor(token, lookups, citationno)
            pdfLinks_list.append(final_pdf_link)
        
        tableHTML = BeautifulSoup(str(tableHTML),"html.parser").prettify(formatter="html")
        tableDf = pd.read_html(tableHTML)
        tableDf = pd.DataFrame(tableDf[0])
        tableDf["PDF links"] = pdfLinks_list
        
        return tableDf


        
        
    def parse(self, response):
        page_source = str(response.body)
        print("hhh = ",page_source)
        
     
# Settings for Running Crawller 
process = CrawlerProcess(settings={'LOG_LEVEL': 'DEBUG',
                                   'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                                   'FEEDS': {"AjioPDP_OutputData.csv": {'format': 'csv', 'overwrite': True}} # For Storing Parse Return Data
                                   })
process.crawl(MyntrapdpSpider)
process.start() 

