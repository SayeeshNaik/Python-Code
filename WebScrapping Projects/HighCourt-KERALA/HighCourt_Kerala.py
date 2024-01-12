import requests
from bs4 import BeautifulSoup
import pandas as pd

def pdfExtractor(token,lookups,citationno):
    pdfURL = '''https://hckinfo.kerala.gov.in/digicourt/Casedetailssearch/fileviewcitation?token={}&lookups={}&citationno={}'''.format(token,lookups, citationno)
    pdfURL = pdfURL.replace("'","")
    return pdfURL

def scrapper(data,apiNum):
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
        final_pdf_link = pdfExtractor(token, lookups, citationno)
        pdfLinks_list.append(final_pdf_link)
    
    tableHTML = BeautifulSoup(str(tableHTML),"html.parser").prettify(formatter="html")
    tableDf = pd.read_html(tableHTML)
    tableDf = pd.DataFrame(tableDf[0])
    tableDf["PDF links"] = pdfLinks_list
    
    return tableDf

def initializer(from_date, to_date):
    url = 'https://hckinfo.kerala.gov.in/digicourt/Casedetailssearch/Orderbyorderdate_ajax/'
    data = {
        'from_date': '{}'.format(from_date),
        'to_date': '{}'.format(to_date),
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
            temp_df = scrapper(data,apiNum)
            main_df = pd.concat([main_df, temp_df])
            main_df.to_excel("TableData ({} to {}).xlsx".format(from_date,to_date))
            print("Scrapped Records = ",apiNum+20,"({})".format(int(lastpageApi)+20))
            apiNum += 20
        except: pass


fromDate = "2023-01-02"
toDate   = "2023-01-03"
initializer(fromDate, toDate)

    
    
    




