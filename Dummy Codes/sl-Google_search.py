from selenium import webdriver

search_string = input("Enter which you want : ")
driver = webdriver.Chrome()

driver.get('https://www.google.com/search?q='+search_string)

option = input('Continue / Close : ')
if(option == 'Continue'):
    print('Browser Running.....')
else : 
    print('Browser Clossed')
    driver.quit()
