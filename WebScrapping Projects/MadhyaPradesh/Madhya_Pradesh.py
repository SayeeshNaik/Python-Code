import requests

url = "https://mphc.gov.in/php/hc/judgement/judgement_pro_afr.php"
data = {
        "date1": "18-07-2023",
        "date2": '20-07-2023',
        "code": "652"
        }

response = requests.get(url,params=data)
print(response.text)