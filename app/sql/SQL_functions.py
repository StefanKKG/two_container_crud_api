# The below library enables us to instantiate and work with the SQLite DB.
import sqlite3
import os
# The below library is used to load data into our Customers table from the csv file with the mock data.
import pandas as pd
cwd = os.getcwd()
#path_to_database = cwd+"/app/var/Database"
path_to_database = cwd+"/var/Database"
path_to_csv = cwd+"/app/data/data.csv"
conn = sqlite3.connect(path_to_database, check_same_thread=False)
cursor = conn.cursor()

print (path_to_database)

def create_table_if_not_exists():
    """
    This function creates the 'Customers' table, unless the table
    already exists, with the below specified column names. 
    """
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Customers (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL,
            address VARCHAR(50) NOT NULL,
            postalZIP VARCHAR(50) NOT NULL,
            region VARCHAR(50) NOT NULL,
            country VARCHAR(50) NOT NULL
        );'''
    )

def load_data_only_once_from_csv_into_db():
    """
    This function ensures that the data from the 'data.csv' file
    is only inserted into the database once.
      
    To do this, the function checks the length of the 'Customers' table. 
    
    If the length of the 'Customers' table is >= 500 (meaning that the csv data is already)
    inserted into the table, then the data is not inserted again.
    """
    df_from_db = pd.read_sql_query("SELECT * FROM Customers;", con=conn)
    if len(df_from_db.index) >= 500:
        pass
    else:
        df_from_csv = pd.read_csv(path_to_csv)
        df_from_csv.to_sql("Customers", con=conn,
                           if_exists="append", index=False)
