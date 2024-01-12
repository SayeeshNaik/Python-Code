from selenium import webdriver
import getpass

username = input("Username : ")
password = input("Password : ")

driver = webdriver.Chrome()
driver.get("https://www.facebook.com/login/")

username_textbox = driver.find_element_by_id('email')
username_textbox.send_keys(username)

password_textbox = driver.find_element_by_id('pass')
password_textbox.send_keys(password)

login = driver.find_element_by_name('login')
login.submit()