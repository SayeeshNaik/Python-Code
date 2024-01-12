from requests_html import HTMLSession
import requests
import pandas as pd
import json
import re

# url = "https://www.ajio.com/search/?text=men%20shirts"
# url = "https://www.ajio.com/dj--c-striped-polo-t-shirt/p/441244133_burntrose"
url = "https://www.ajio.com/the-bear-house-checked-slim-fit-shirt/p/464175602_grey"


All_ProductID = list(pd.read_excel("Ajio_ProductID.xlsx")['ProductId'])

logical_df = {
    'Title' : '{"altText":',
    'Brand' : '{"brandName":',
    'MRP' : '","formattedValue',
    'Discount': ',"discountPercent"',
    "Sizes": '"scDisplaySize":',
    'Details': '"comparable":true,"featureValues":[{"value":"',
    
    }

main_df = pd.DataFrame()
exception_id = []
def scrapper(productId):
    url = "https://www.ajio.com/p/{}".format(str(productId))
    page = requests.get(url)
    page = str(page.content)
    start_ind = page.index('{"wishlist":{}')
    end_ind = page.index('"unRatedProducts":""}}')+22
    data = page[start_ind:end_ind]
    temp_dict ={}
    
    try:
        temp_dict.update({"Product_Id": productId})
        for key in logical_df:
            logic = logical_df[key]
            l = data.count(logic)
            if(key=='MRP'):  
                amount_lis=[m.start() for m in re.finditer(logic, data)]
                val1 = list(map(int, re.findall(r'\d+', data[amount_lis[0]:amount_lis[0]+40])))
                val1=int(''.join(map(str,val1[0:len(val1)-1])))
                val2 = list(map(str, re.findall(r'\d+', data[amount_lis[1]:amount_lis[1]+40])))
                val2=int(''.join(map(str,val2[0:len(val2)-1])))
                if(val1>val2):temp_dict.update({key: val1})
                else: temp_dict.update({key: val2})
                if(val1<val2):temp_dict.update({'Price': val1})
                else: temp_dict.update({'Selling Price': val2})
            elif(key=='Details'):
                # val = data[data.find(logic):data.find(logic)+200].split(':')[3].split(',')[0]
                val_ind = [i for i in range(len(data)) if data.startswith(logic, i)]
                val = []
                for ind in val_ind:
                    ind += len(logic)
                    val.append(data[ind:ind+500].split('"}]}')[0])
                    print(val)
                temp_dict.update({key: val})
            elif(key=='Sizes'):
                val_ind = [i.start() for i in re.finditer(logic, data)]
                val = []
                for ind in val_ind: val.append(data[ind:ind+21].split(':')[1].replace(',',''))
                temp_dict.update({key: val})
            else:
                val = data[data.find(logic):data.find(logic)+200].split(':')[1].split(',')[0]
                temp_dict.update({key: val})
    except: exception_id.append(productId)
    print(temp_dict)
    
for ind in range(2):
    scrapper(All_ProductID[ind])