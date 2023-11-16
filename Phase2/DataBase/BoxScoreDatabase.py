import conncect_db
import pandas as pd
import numpy as np




# Connect to the SQLite database
conn_Main,cursor_Main = conncect_db.connect_to_database('Main')
conn_BoxScores,cursor_BoxScores = conncect_db.connect_to_database('BoxScores')

# Execute a SELECT query to retrieve all values in the 'Token' column
cursor_Main.execute('SELECT Token FROM schedule WHERE Winner IS NOT NULL')

# Fetch all the results
tokens = cursor_Main.fetchall()
conncect_db.close_database_connection(conn_Main)
# Iterate through the tokens
"""
conn_BoxScores.execute(f'DROP TABLE IF EXISTS BoxScores')
cursor_BoxScores.execute(f'''
    CREATE TABLE IF NOT EXISTS BoxScores (
        boxscore_id VARCHAR(255) PRIMARY KEY,
        "Player" TEXT,
        "MP" TEXT,
        "FG" REAL,
        "FGA" REAL,
        "FG%" REAL,
        "3P" REAL,
        "3PA" REAL,
        "3P%" REAL,
        "FT" REAL,
        "FTA" REAL,
        "FT%" REAL
        "ORB" REAL,
        "DRB" REAL,
        "TRB" REAL,
        "AST" REAL,
        "STL" REAL,
        "BLK" REAL,
        "TOV" REAL,
        "PF" REAL,
        "PTS" REAL,
        "+/-" TEXT
        
    )
''')

conn_BoxScores.commit()
"""
for t in tokens:
    tok = t[0]
    

    box_df = pd.read_csv(f"/Users/roy/Desktop/SPIDE/BoxScores/{tok}.csv",header=None,skiprows= 1)
    new_row = [np.nan, "Basic Box Score Stats"] + [np.nan] * (len(box_df.columns) - 2)

    # Insert the new row at the beginning
    box_df.loc[-1] = new_row
    box_df.index = box_df.index + 1  # Shift the index to accommodate the new row
    box_df = box_df.sort_index() 
    current_header = None
    current_dataframe = None
    dataframes = {}
    home=tok[9:12]
    away=tok[-3:]
    
    header_titles=["G","Q1","Q2","H1","Q3","Q4","H2"]
    ind=0
    flag=away
    # Iterate through rows
    for index, row in box_df.iterrows():
    
        if 'Basic Box Score Stats' in row[1]:
            # If a new header is found, save the current dataframe (if any)
            # and create a new one with the new header
            if current_header is not None:
                dataframes[current_header] = current_dataframe
            if ind==len(header_titles):
                ind = 0
                flag = home 
            current_header = header_titles[ind]+"_"+flag
            
            ind+=1
            current_dataframe = pd.DataFrame(columns=box_df.columns)
        else:
            # Append the current row to the current dataframe
            current_dataframe = current_dataframe.append(pd.Series(row, index=box_df.columns), ignore_index=True)

    # Save the last dataframe
    if current_header is not None:
        if current_header not in dataframes:
            dataframes[current_header] = current_dataframe
    

    for k in dataframes:
        new_column_names = dataframes[k].iloc[0]
        new_column_names[0] = "Player"
        mask = dataframes[k][2]!= 'FG'
        df = dataframes[k][mask]
        df.rename(columns=dict(zip(df.columns, new_column_names)), inplace=True)
        
        df.to_sql(f'Box{tok}_{k}', conn_BoxScores, if_exists='replace', index=False)

conncect_db.close_database_connection(conn_BoxScores)


																			