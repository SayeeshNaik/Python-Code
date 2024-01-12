import requests

url = "https://highcourt.hp.gov.in/causelist/nextnetbd.php"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "hidden=value; PHPSESSID=akqtrlctkvc6ip13s52b69micl",
    "Origin": "https://highcourt.hp.gov.in",
    "Referer": "https://highcourt.hp.gov.in/causelist/netbd.php",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "sec-ch-ua": '^"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

data = {
    "m_juris": "S",
    "m_causetype": "D",
    "m_sideflg": "C",
    "frm_action2": "",
    "m_causedt": "10-08-2023"
}

response = requests.post(url, headers=headers, data=data, verify=False)  # Note: Disabling SSL verification for demonstration purposes

print(response.text)
