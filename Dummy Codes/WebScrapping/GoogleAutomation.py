from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
lis = ['mysore','ambani','fdfafdfe','fdsarew','programiz','ertewxd','ewrewfdsa','shivamg','shivamogga']
valid_lis,invalid_lis = [],[]
corrected_lis = []
for word in lis:
    driver.get("https://www.google.com/search?q="+word)
    try:
        driver.find_element(By.CLASS_NAME,'gL9Hy')
        invalid_lis.append(word)
        corrected = driver.find_element(By.XPATH,'//*[@id="oFNiHe"]/p/a').text
        corrected_lis.append({word:corrected})
    except:valid_lis.append(word)    
print(' Valid Words : ',valid_lis)
print('Invalid Words : ',invalid_lis)
print("You can Use Insted of this Words : \n",corrected_lis)

