import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


data = {
    'jcode': '599',
    'frdate': '01/08/2023',
    'todate': '07/08/2023'
}

response = requests.post('https://dhcappl.nic.in/dhcorderportal/judname.do', data=data)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find("table")

data = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    cells = row.find_all('td')
    # print(row.find("a"))
    item = {
        'Name': cells[0].get_text().strip(),
        'Age': cells[1].get_text().strip(),
        'Country': cells[2].get_text().strip()
    }
    data.append(item)

json_data = json.dumps(data, indent=4)
df = pd.DataFrame(json.loads(json_data))
df.to_excel("Delhi.xlsx")
print(df)


