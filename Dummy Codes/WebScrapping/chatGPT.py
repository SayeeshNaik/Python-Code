from bs4 import BeautifulSoup
import requests


# html = requests.get('https://www.google.com/search?q=how+to+convert+set+to+list+in+javascript&rlz=1C1GCEA_enIN972IN972&ei=xN7jY8ONH5ycseMP5ZWNiAw&ved=0ahUKEwjD_6evvIb9AhUcTmwGHeVKA8EQ4dUDCA8&uact=5&oq=how+to+convert+set+to+list+in+javascript&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQgAQyCQgAEBYQHhDxBDIFCAAQhgMyBQgAEIYDMgUIABCGAzIFCAAQhgM6CggAEEcQ1gQQsAM6BAgAEEM6CAgAEBYQHhAKOgYIABAWEB5KBAhBGABKBAhGGABQlAFYhBxghx1oAXABeACAAYoBiAHZDJIBBDAuMTSYAQCgAQHIAQjAAQE&sclient=gws-wiz-serp')
html = requests.get('https://stackoverflow.com/questions/20069828/')
soup = BeautifulSoup(html.text, 'html.parser')

answers = soup.find_all(class_="answercell post-layout--right")
for answer in answers:
  print(answer.find_all("code")[-1].text)
# with open("chatGPT.html","w") as f:
#     f.write(str(answer[0]))

# ans = soup.find_all(class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf")
# print(ans)