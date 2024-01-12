import requests

followers_count = 100
url = f"https://www.instagram.com/api/v1/friendships/11390065969/followers/?count={followers_count}"

headers = {
    "authority": "www.instagram.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "cookie": "mid=ZK_WdwALAAE4sqJD9OGB99GUoahG; ig_did=AADFEA6C-0AF1-4B4E-BF25-908C90FA3D3A; ig_nrcb=1; datr=XYm1ZJjF3-ykvRCO-_hL0YrN; csrftoken=mc0ZXykp2gNStqlnkmb0mQVJvoMj2Cqk; ds_user_id=10655002964; dpr=1.3499999046325684; shbid=^78^\"10655002964^,^1735500640:01f7e7eb9808efc046a13b9313607d69d702199c36a638681435a2e7b5e5d01d4658161e^\"; shbts=^\"1703964640^\"^,^10655002964^,^1735500640:01f78bb59c86cad8d4e58c453d0a03b565e2d7a9a9b17f00bd6e071238c9162dddb643b0^\"; sessionid=10655002964%3A7B4uIRZl21flou%3A27%3AAYd9X4EzPzH01ZPf5C5tUuPtkfRzQQgNJ8W1xq25bA; rur=^\"CCO^\",^10655002964^,^1735500882:01f7f4ba2744d83a9f59a8c989f4ae1d09d21b6cf0f31b794ada6067b88dd54ec508a49e^\"",
    "dpr": "1.35",
    "pragma": "no-cache",
    "referer": "https://www.instagram.com/sayeesh14/followers/",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-full-version-list": "\"Not_A Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"120.0.6099.130\", \"Google Chrome\";v=\"120.0.6099.130\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"15.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "viewport-width": "688",
    "x-asbd-id": "129477",
    "x-csrftoken": "mc0ZXykp2gNStqlnkmb0mQVJvoMj2Cqk",
    "x-ig-app-id": "936619743392459",
    "x-ig-www-claim": "hmac.AR2nQI1REjvtMXbnoXwpUTmFty_X1xownTVV1TPULmr-qzOT",
    "x-requested-with": "XMLHttpRequest"
}

try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        username_dict = {}
        data = response.json()
        data = data['users']
        for each_data in data:
            username_dict.update({each_data['full_name']:each_data['username']})
        print(username_dict)
        print(len(username_dict))
    else:
        print("Error")

except Exception as e:
    print(f"An error occurred: {e}")
