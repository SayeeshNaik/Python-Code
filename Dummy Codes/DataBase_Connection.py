import psycopg2 as pg
from sqlalchemy import create_engine
import pandas as pd

hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = '12345'
port_id = 5433

try:
    # Create an SQLAlchemy engine
    engine = create_engine(f'postgresql+psycopg2://{username}:{pwd}@{hostname}:{port_id}/{database}')

    # Connect using psycopg2 for table creation and data insertion
    conn = pg.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )

    print("Connection opened successfully...!!\n")

    cur = conn.cursor()

    # Queries
    create_table_query = '''CREATE TABLE students (
                                name varchar(50),
                                age int,
                                marks int
                            ); '''

    insert_query = '''INSERT INTO students (name, age, marks) VALUES('pavan', 22, 90)'''

    table_data_query = '''SELECT * FROM students'''
    
    drop_duplicates_query = '''SELECT DISTINCT * FROM students'''
    
    clear_all_row_query = '''TRUNCATE TABLE students'''
    
    delete_whole_table = '''DROP TABLE students'''



    # Read data into a Pandas DataFrame
    data = pd.DataFrame(pd.read_sql(table_data_query, engine))
    print(data)
    data.drop_duplicates(inplace=True)
    print(data)
    
   

    # print(data)
    

    ### Executes Query
    # cur.execute(insert_query)
    
    ### DF To SQL
    # data.to_sql(name='students', con=engine, if_exists='replace', index=False)

    # Commit changes to the database
    conn.commit()

except Exception as err:
    print('Error:', err)

finally:
    # To Close the database connection
    conn.close()
    print("\nConnection closed...!!")
