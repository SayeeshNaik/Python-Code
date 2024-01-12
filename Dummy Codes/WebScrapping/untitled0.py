import json
import codecs
from cleantext import clean

txt = "https:u002Fu002Fassets.myntassets.comu002Fassetsu002Fimagesu002F2023u002F1u002F28u002F1d1d1e3f-ac8a-4c07-8d7c-e7398fa3b0951674911520148-photo_6244437756516349297_y.jpg"
ans = txt.encode("ascii","ignore")
ans = ans.decode()
# print(txt.encode().decode('unicode-escape'))

data = '{"Name":"Sayeesh\'"}'
data = clean(data,no_emoji=True,lower=False)
print(json.loads(data))