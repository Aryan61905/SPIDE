import conncect_db
import pandas as pd
import numpy as np



conn,cursor = conncect_db.connect_to_database("Main")
df = pd.read_csv("/Users/roy/Desktop/SPIDE/Phase2/csvs/TeamStats.csv")
df.to_sql('Teams', conn, if_exists='replace', index=True)

conncect_db.close_database_connection(conn)