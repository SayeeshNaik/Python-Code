import psycopg2 as pg
import psycopg2.extras
import pandas as pd
import os
from pathlib import Path
from sqlalchemy import create_engine

hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = 12345
port_id = 5432

conn = pg.connect (
                    host = hostname,
                    dbname = database,
                    user = username,
                    password = pwd,
                    port = port_id
                  )
cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
engine = create_engine("postgresql://postgres:12345@127.0.0.1/postgres")

def engineData(path):
    try:
        
        df = pd.read_excel(path)
        df.reset_index(drop=True, inplace=True)
        print(df)
        df.to_sql(name="company",con=engine,schema="public",if_exists="append")
    except:
        pass
    
def drop(path):
    table_name = Path(path).stem
    q = 'Drop table '+ table_name
    try:
        cur.execute(q)
        conn.commit()
        print(table_name," : Dropped Table")
    except:
        pass

folder = "C:/Users/User/Myexcel/"
for path in os.listdir(folder):
        if path.endswith(".xlsx"):
            path = folder + path
            drop(path)
            engineData(path)