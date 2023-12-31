from doctest import debug_script
from json import load
from pydoc import describe
from quopri import decodestring
import pandas as pd
import psycopg2

def loadData():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="tellco",
        user="postgres",
        password="root"
    )
    #cursor = conn.cursor()
    cursor = conn.cursor('my_cursor_name', withhold=True)
    cursor.execute("SELECT * FROM xdr_data")
        # Fetch a batch of rows
    batch_size = 1000
    rows = cursor.fetchmany(batch_size)
    
    data = [] 

    while rows:
        # Process the fetched data
        data += rows
        # Fetch the next batch
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        if len(data) >= 50000:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=columns)
            return df

    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()  
    df = pd.DataFrame(data, columns=columns) 
    print(len(data))
    
    return (df)




