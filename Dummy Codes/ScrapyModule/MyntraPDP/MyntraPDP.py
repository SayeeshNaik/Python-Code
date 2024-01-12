from requests_html import HTMLSession
import requests
import pandas as pd
import json
import re

main_url = "https://www.myntra.com/2498520"
page = str(HTMLSession().get(main_url).content)
login_df = {"Product Details":'"articleAttributes":'}

st_ind = page.find(login_df['Product Details'])+len(login_df['Product Details'])
data = page[st_ind:].split("}")[0]+'}'
data = json.loads(data)
specification = ['Fabric','Length','Multipack Set','Number of Pockets','Pattern','Sleeve Length',
 'Surface Stying','Fit','Main Trend','Neck','Occasion','Print or Pattern Type','Sleeve Styling',
 'Wash Care']
print(data)
for key in specification:
    try:
      print(key,data[key])
    except: pass



















