
import psycopg2 as pg
import psycopg2.extras
from sqlalchemy import create_engine

# class db:
      # def connection():
hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = 12345
port_id = 5432

try:
    conn = pg.connect (
                        host = hostname,
                        dbname = database,
                        user = username,
                        password = pwd,
                        port = port_id
                      )
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    engine = create_engine("postgresql://postgres:12345@127.0.0.1/postgres")
    print('Connected Successfully')
    
except:
    print('Error while Connecting DataBase')
            