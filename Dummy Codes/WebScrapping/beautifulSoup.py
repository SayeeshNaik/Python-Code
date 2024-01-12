import requests
from bs4 import BeautifulSoup

link = "https://www.dhiomics.com"
# link = "https://www.dhiomics.com/"
html = requests.get(link)
soup = BeautifulSoup(html.content, 'html.parser')
# print(html.status_code)

# Parsing the HTML
# print(soup.prettify())

with open('DhiomicsWebScrapping.csv','w') as file:
    file.write(soup.prettify())

#tag name 
# print(soup.find_all('link'))

#get Text by class or Id
# print(soup.select('#testimonial1'))
# print(soup.find(id='testimonial1'))
# print(soup.find(class_='testimonial').find('p').text)
# title = soup.find("span", attrs={"id":'productTitle'})
# soup.h2.get('class')
# print(soup.find_all('p'))

# pTags = []
# [pTags.append(i.get_text()) for i in soup.find_all('p')]
# for i in pTags:
#     print(i)

#All Links
# for i in soup.find_all('a'):
#     print(i.get('href'))

# Inside Element Key    
# print(soup.find('a').get('class'))


# ------------------------------------

# link = "https://assam.gov.in/list-of-secretaries"
# html = requests.get(link)
# soup = BeautifulSoup(html.content, 'html.parser')

# tb = soup.find('table')
# print(tb)
# th = soup.find_all('th')
# print(len(th))
# td = soup.find_all('td')
# print(len(td))
# tr = soup.find_all('tr')
# print(len(tr))
# col_lis = []
# for col in th:
#     col_lis.append(col.text)

# Func = open("my.html","w")

# Func.write(str(tb))
# 			
# Func.close()

