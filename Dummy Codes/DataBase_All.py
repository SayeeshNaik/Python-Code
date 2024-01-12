import psycopg2 as pg
import psycopg2.extras
import pandas as pd
import os
from pathlib import Path

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

def xlData(path):
    table_name = Path(path).stem
    df = pd.read_excel(path)
    head = tuple(df.columns)
    col=''
    for i in head:
        col += str(i)+' varchar,'
        
    q = '('+col+')'
    print(q)
    q = q.replace(q[0:-1], q[0:-2])

    query = 'Create Table ' + table_name + q
    try:
        cur.execute("rollback")
        cur.execute(query)
        conn.commit()
        print(table_name," : Table Created Successfully")
        insert(path)
    except:
        print(table_name, " : Table Name Already Exist")
        insert(path)
    
def insert(path):
    table_name = Path(path).stem
    df = pd.read_excel(path)
    head = tuple(df.columns)
    
    v=[]
    col = ''
    for k in range(len(head)):
        col += head[k] + ', '
    col = '(' + col[0:-2] + ')'
    truncate(table_name)
    for i in range(len(df)):
        for j in head:
              v.append(df[j][i])
        val = str(tuple(v))
        v.clear()
        insert_query = 'Insert Into ' + table_name + col + ' Values ' + val
        cur.execute(insert_query)  
        conn.commit()
    print(table_name," : Data Inserted Successfully")
           
def truncate(table_name):
    q = 'Truncate table '+ table_name
    cur.execute(q)
    conn.commit()
    
def drop(path):
    table_name = Path(path).stem
    q = 'Drop table '+ table_name
    try:
        cur.execute(q)
        conn.commit()
        print(table_name," : Dropped Table")
    except:
        pass

def DbTableRead():
    table_name = input("Enter Table Name : ")
    try:
        query = 'Select * From '+ table_name
        cur.execute("rollback")
        cur.execute(query)
        conn.commit()
        df = pd.read_sql_query("SELECT * from "+table_name, conn)
        df = df.to_string(index=False)
        print(df)
    except:
        print(table_name," Table is Not Exist")
        pass
    
# Main 
# folder = "C:/Users/User/Myexcel/"
# folder = "C:/Users/User/Downloads/Govind.xlsx"
# for path in os.listdir(folder):
#         if path.endswith(".xlsx"):
#             path = folder + path
#             xlData(path)
#             print(path)

xlData("C:/Users/User/Downloads/Govind.xlsx")
         
            

