import re
import urllib.request
response = urllib.request.urlopen('https://www.ajio.com/p/460453610_white')
html = response.read()
text = html.decode()
print(text)