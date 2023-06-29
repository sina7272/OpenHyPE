import psycopg2
import pandas.io.sql as psql
import pandas as pd
import credentials as creds
from queries import *
#from logger import logger

# Set up a connection to the postgres server.
conn_string = "host=" + creds.PGHOST + " port=" + "5432" + " dbname=" + creds.PGDATABASE + " user=" + creds.PGUSER \
    + " password=" + creds.PGPASSWORD
conn = psycopg2.connect(conn_string)
print("Connected to server!")

# Create a cursor object
cursor = conn.cursor()
def get_table_nitrat(schema):
    query = "select * from hygrisc.nitrat_long"
    df = pd.read_sql(query, conn)
    cursor.close()
    return df


def get_table_sulfat(schema):
    query = "select * from hygrisc.sulfat_long"
    df = pd.read_sql(query, conn)
    cursor.close()
    return df

