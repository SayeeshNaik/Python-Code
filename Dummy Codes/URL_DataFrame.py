from urllib.request import urlopen
import json
import pandas as pd
from sqlalchemy import create_engine

url = "https://gorest.co.in/public/v2/todos"
xl_path = "D:/FlaskProject-1/URL_To_DB/URL_To_DB.xlsx"
  
response = urlopen(url)
data_json = json.loads(response.read())

# DataFrame 
df = pd.DataFrame(data_json)
exl = df.to_excel(xl_path)
print(df)

# DB Logic
engine = create_engine("postgresql://postgres:12345@127.0.0.1/postgres")

# def engineData(path):
#     try:
#         table_name = input("Enter Table Name : ")
#         df = pd.read_excel(path)
#         df.reset_index(drop=True, inplace=True)
#         print(df)
#         df.to_sql(name= table_name, con=engine, schema="public" ,if_exists="append")
#     except:
#         pass

# # Calling Function
# engineData(xl_path)