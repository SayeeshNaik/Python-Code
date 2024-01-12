import requests

url = "https://www.justdial.com/api/detail?searchReferer=gen^%7Clst"
headers = {
    "authority": "www.justdial.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "cookie": '''ppc=; _ctok=5c4bfc8867ec89ffcb1f21dbc382b26fa27cb79f08d253101c6e0e2eae1a6be8; scity=Chennai; inweb_city=Chennai; pincode=; alat=; alon=; sarea=; web_visit=2023-11-02T12:37:53.014Z; jd_www_nxt=1; bm_sz=149899A3BEDED5CFE3535456BD37FF83~YAAQFzkgF5x4JH+LAQAAN0IKkBVEz9kX5omlK3mqdBD4lsNWDnLeblFr3lhafiQouA+X/ANkK0H/pmC9OcL5j00iTujhKQtM0vGn0GvSB+D/IBHa/tj4iiNRHFvmnKQGNgqNJFqwRhjUxYiLDKwzLsl/GuKhoz+3zx/BU4FHNFSOnLyr2gIZ5eArPvJkyVU6Qa3vVCL58Up8kImJ1R78Js4PmsXip3AKD9IuxKeLPjY9HUH95+WePI5i7XgO1QfyPAL86Ilr5gQFwi6lOP7hevMnn1r416pwUtPM3axQF8kkm7bJLw==~3747907~4408645; _gid=GA1.2.2060592498.1698928672; lpg=lst; rfr=gen; Continent=AS; Ak_City=CHENNAI; TKY=58d7b3d6f3290f4d1a0939a6f925d85b9c81f970081fe8d14ee87612ad9a0d10; main_city=Chennai; docidarray=; sid=; ppc=; ak_bmsc=4F459F34162D9175B55CBE82D10D1420~000000000000000000000000000000~YAAQTDkgF3qXgo+LAQAAeRgpkBUuuUyw+tpqK5nB0cgwuhhvfR8Bm8sLzI50HDBSGr79jhk6co1E0cMadlU1+vEQhxaiBwIcL350Hh8j4mr0EmmtigMscceM4dRMqLucWLrlMOBVk6kj/eO9maPB7y7sBVPDZ3sLzj020VEoq+P/cnyJGev7CPgFOcW5BHVT3K+avXNJkwH204jSGIHu2vF1qHYuirxErupfnpPjVcWLYcgboDPxapZhj54RG9dsehreOt5704GJ59aVwwy4UbjJ/qOvvfVPA+SVgGQrny0wDcb4o8tjA92rTLYxuF63vyWCmdSZFlqzLtGwIfrItoaGoi1Lzcbg+efhTe+uIGjwZdPmQ4D5zt/u5zH5+PX1bvayw31s942eRG/ycE7jopwacmdpjB66xB4VrFy2HEFHoNYbxpStKKdi6O/VG6GiMh4EylHvMDTw6/KnHHW/STjNllUyEW2OGlPaILVRvtUZDrXpN8TbWGQgbTdeNYRH4K5l8uVl17WFSCWtnBXjhYZoIw==; touch=2450368704.11043.0000; AKA_A2=A; _abck=44B0B46B5F624250481B1F3680CA8913~0~YAAQPTkgF4Wih2qLAQAAAFRFkAobkYC5l8pHVghmWjmH5wE954udofixONEWg3WnfucVwdZN+BrCcUhhC2/TZHwHnV03cZrQOQ57NYJOK736yjQSsvRzzFoIT0rH/P+r3Qfet9q75r5NIctvOQGCEPxphPAAlsWJI3qfrQ9ZfU/cx+CM3Ko/Yrh2ljXR3gFmQaTmQc23MCyXoMgodnQYl8dlWniwnVfwMz5pdPFDcD9JYECLnGjl/2ThMr0xjXdLP3CVEEpq0TTQO6XTCt8VsWr9GPIVq3hMQnDrJdqHNODHjmNrX563RcDs0Iqs9qhOu5vnKMJRA5r2uJdnhZ/aoCjTwkfvdH3GAfr2a2mzebwpFn3O3uhWk6bS0cL3hvi0gsPVBxhEtM1EvTgV03YPYIofqekmareT3XwGhIwA3g==~-1~-1~-1; RT="z=1&dm=justdial.com&si=a49776f9-f094-4110-a300-8dc1c4174e9f&ss=loh69kf4&sl=7&tt=1mx&obo=6&rl=1"; _ga=GA1.1.2069705524.1698928672; _ga_5PY4KYQRFS=GS1.1.1698932418.3.1.1698932630.59.0.0; bm_sv=F8D79FD6CE4F67402D991A9BD25CABEF~YAAQPTkgFyG5h2qLAQAAlQdIkBUnjXJZqumejcNc0hkuYHq998q6LmFMPxesN8PlLHxwL7tcql1BDWKyHG+ddDHZ5r4ohC0rcHUcx6k5gnfjm4bPipotM2+WR5EVxuYvAE/AySTXD9LMrGHjue6lbuZGZao6iZ+D9AXVGj3IudzdJvQDGbLYdjexZFQLRquxsbcWg6Sx7/gD2NYff8Jl0T9Qj7OhbT849Zi9NWBGZkUduOBlE8q/RloWkf5q3RC+LKTtsg==~1''',
    "origin": "https://www.justdial.com",
    "pragma": "no-cache",
    "referer": "https://www.justdial.com/Chennai/Trendzdeck-Designer-Studio-Boutique-Fashion-Designing-Institute-Beside-Sivan-Temple-Valasaravakkam/044PXX44-XX44-190603163639-C1W5_BZDET?ncatid=10892820&area=&search=Top%20Fashion%20Designer%20Stores%20in%20Chennai&mncatname=Fashion%20Designer%20Stores&search_id=4b905a63f04362f774f765655c37e06279985c6b974ed5be8d8983f419261368&abd_btn=&abd_heading=",
    "requesttime": "2023-2-11^6^3:52:43 PM",
    "sec-ch-ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "securitytoken": "2a282a2b2a29292e2d2a2c2b",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

data = {
    "city": "Chennai",
    "search": "Trendzdeck-Designer-Studio-Boutique-Fashion-Designing-Institute-Beside-Sivan-Temple-Valasaravakkam",
    "docid": "044PXX44.XX44.190603163639.C1W5",
    "ncatid": "10892820",
    "catname": "Fashion Designer Stores",
    "mobile": "",
    "bid": 0,
    "pdid": [],
    "search_id": "4b905a63f04362f774f765655c37e06279985c6b974ed5be8d8983f419261368"
}

response = requests.post(url, headers=headers, json=data)
with open('pavanTest.txt','wb') as file:
    file.write(str(response.text))
    
print(response.text)
