# from selenium import webdriver
# from selenium.webdriver.common.by import By

# # url = "https://www.ajio.com/search/?text=mens%20shirt"
# url1 = "https://www.myntra.com/10787894?bm-verify=AAQAAAAG_____zRjr3yG0nEp919XG9fdS2bTdPDdxWOYyF0quN-RXh6oLSXdYSUGoY3Ubpxh0DkNSWTm2bcniRAIrSFgiv9wON0Q88pcr9ZnjA0hQFY8fzdqO1-Ur02kP1Lo_-Y6eP_Xus-p6rhicA5n3M7gvovoZGkE5E6ngzx481D8WNtSK6YPo_ebWY7BUQpyyKbeIETNnpxOwgaBKFWZ3SI0AwRzLTvcW_CEDj0-0QN5UAQ2"
# url2 = ""
# driver = webdriver.Chrome()
# driver.get("https://www.myntra.com/10787894?bm-verify=AAQAAAAG_____zRjr3yG0nEp919XG9fdS2bTdPDdxWOYyF0quN-RXh6oLSXdYSUGoY3Ubpxh0DkNSWTm2bcniRAIrSFgiv9wON0Q88pcr9ZnjA0hQFY8fzdqO1-Ur02kP1Lo_-Y6eP_Xus-p6rhicA5n3M7gvovoZGkE5E6ngzx481D8WNtSK6YPo_ebWY7BUQpyyKbeIETNnpxOwgaBKFWZ3SI0AwRzLTvcW_CEDj0-0QN5UAQ2")
# # driver.get(url)
# # main_div = "//a[@class='rilrtl-products-list__link']"
# # all_div = driver.find_elements(By.XPATH,main_div)
# # productId_lis = []
# # for div in range(1,len(all_div)+1):
# #     myXpath = main_div+'[{}]'.format(div)
# #     driver.find_element(By.XPATH,myXpath).click()
# #     baseUrl = driver.current_url
# #     print(baseUrl)
# #     # productId = baseUrl.split("/p/")[1]
# #     # productId_lis.append(productId)
# #     # print(productId)

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

path = "C:/Users/User/Scrapy Websites/www.flipkart.com/"
product_id = pd.read_csv(path+"FlipkartPDP_Exception_ProductID.csv")
product_id = list(product_id['Exception_ProductID'])

main_url = 'https://www.flipkart.com/x/p/k?pid='
driver = webdriver.Chrome()
exp_lis = []
output_lis = []
for p_id in product_id[0:1]:
    temp_dict = {}
    driver.get(main_url+p_id)
    temp_dict.update({"URL":main_url+p_id})
    for key in ['brand','title','mrp']:
        try:
            if(key=='brand'): val = driver.find_element(By.XPATH,"//span[@class='G6XhRU']").text
            # if(key=='mrp'): val = driver.find_element(By.XPATH,"//div[@class='_25b18c']//div[2]").text
            elif(key=='title'): val = driver.find_element(By.XPATH,"//span[@class='B_NuCI']").text
            # elif(key=='title'): val = driver.find_element(By.XPATH,"//span[@class='B_NuCI']").text
            else: val = driver.find_element(By.XPATH,"//div[@class='_30jeq3 _16Jk6d']").text
            # else: val = driver.find_element(By.XPATH,"//span[@class='B_NuCI']").text
        except: 
            val = '***'
            exp_lis.append(p_id)
        temp_dict.update({key: val})
    output_lis.append(temp_dict)    
driver.close()
exp_lis = list(set(exp_lis))       
print(len(exp_lis),'\n',exp_lis)
print(len(output_lis),'\n',output_lis)
