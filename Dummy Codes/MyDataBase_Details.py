import psycopg2 as pg
import psycopg2.extras

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
