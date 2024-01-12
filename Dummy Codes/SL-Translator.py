from selenium import webdriver

language = input('Enter Exist language : ')
convert  = input('Enter to convert language : ')
sentence = input("Enter your sentence : \n")
driver = webdriver.Chrome()
driver.get("https://www.google.com/search?q="+language+'+'+convert+'+'+"translate")
translator = driver.find_element_by_id('tw-source-text-ta')
translator.send_keys(sentence)

