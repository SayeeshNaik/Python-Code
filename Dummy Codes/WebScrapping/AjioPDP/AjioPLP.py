import requests
import json
import pandas as pd


df = pd.read_excel("AjioPLP_KeyName.xlsx")
keyname_lis = list(df['Key_Name'])
# keyname_lis = keyname_lis[1:2]
keyname_lis = ['women dress']
urls = []
for keyname in keyname_lis: 
    # url = "https://www.ajio.com/api/search?fields=SITE&currentPage=1&pageSize=45&format=json&query={0}&sortBy=relevance&text=militry&gridColumns=3&advfilter=true&platform=Desktop&is_ads_enable_plp=false&is_ads_enable_slp=false&showAdsOnNextPage=false&segmentIds=".format(keyname)
    url = "https://www.ajio.com/api/search?fields=SITE&pageSize=45&format=json&query={0}&sortBy=relevance&gridColumns=3&advfilter=true&platform=Desktop&is_ads_enable_plp=false&is_ads_enable_slp=false&showAdsOnNextPage=false&segmentIds=".format(keyname)
    urls.append(url)
   

output_data = []
exception_url = []
for url in urls:
    for page_num in range(1,2):
        url = url+("&currentPage={}".format(str(page_num)))
        print("******************************")
        print(url)
        data = requests.get(url)
        json_data = data.json()
        # print(json_data['products'])
        try:
            for product in json_data['products']:
                print(product['name'])
                output_data.append(product['name'])
        except: exception_url.append(url)
    output_data.append("################################")
    

pd.DataFrame({'Title':output_data}).to_excel('AjioPLP_Data.xlsx',index=False)
pd.DataFrame({'Exception_URL':exception_url}).to_excel('AjioPLP_ExceptionURL.xlsx',index=False)