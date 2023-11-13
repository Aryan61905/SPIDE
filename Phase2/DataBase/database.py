import sqlite3

# Create a new SQLite database or connect to an existing one
conn = sqlite3.connect('NBA_Player_Database.db')
cursor = conn.cursor()

# Create a Players table based on the columns you provided
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Players (
        player_id INTEGER PRIMARY KEY,
        "Player" TEXT,
        "Pos" TEXT,
        "Age" INTEGER,
        "Tm" TEXT,
        "G" INTEGER,
        "GS" INTEGER,
        "MP" REAL,
        "FG" REAL,
        "FGA" REAL,
        "FG%" REAL,
        "3P" REAL,
        "3PA" REAL,
        "3P%" REAL,
        "2P" REAL,
        "2PA" REAL,
        "2P%" REAL,
        "eFG%" REAL,
        "FT" REAL,
        "FTA" REAL,
        "FT%" REAL,
        "ORB" REAL,
        "DRB" REAL,
        "TRB" REAL,
        "AST" REAL,
        "STL" REAL,
        "BLK" REAL,
        "TOV" REAL,
        "PF" REAL,
        "PTS" REAL,
        "COMBO" TEXT
    )
''')

conn.commit()

import pandas as pd
import sqlite3

# Connect to the SQLite database


# Read the CSV data
df = pd.read_csv("/Users/roy/Desktop/SPIDE/OverallPlayerStats.csv")

# Insert the data into the Players table
df = df[df.PTS != "PTS"]
df["TRB"] = df["TRB"].astype(float)
df["PTS"] = df["PTS"].astype(float)
df["AST"] = df["AST"].astype(float)

df["COMBO"] = (df["PTS"])+(df["AST"])+(df["TRB"])
df = df.sort_values(by=["COMBO"],ascending=False)

df.to_sql('Players', conn, if_exists='replace', index=False)


conn.close()