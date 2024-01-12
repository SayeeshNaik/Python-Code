import pandas as pd
import json
from urllib.request import urlopen
from sqlalchemy import create_engine

url = "https://gorest.co.in/public/v2/todos"
response = urlopen(url)
data = json.loads(response.read())
print(data)
engine = create_engine("postgresql://postgres:12345@127.0.0.1/postgres")
df = pd.DataFrame(data)
df.to_sql(name="MyTesting", con=engine)
print(df)
