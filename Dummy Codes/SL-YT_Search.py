from selenium import webdriver

search_string = input('Enter the Topic : ')

driver = webdriver.Chrome()
driver.get("https://www.youtube.com/results?search_query="+search_string)
