import pandas as pd
import pandas.io.sql as sqlio
import psycopg2 as ps
from langchain.sql_database import SQLDatabase


connection = ps.connect(dbname='postgres',
                        user='postgres',
                        password='123',
                        host='localhost',
                        port='5432')

connection_string = 'postgresql://postgres:123@localhost:5432/postgres'

# Create an instance of SQLDatabase
sql_database = SQLDatabase.from_uri(connection_string)