import conncect_db
import pandas as pd
import numpy as np




# Connect to the SQLite database
conn,cursor = conncect_db.connect_to_database('Main')

cursor.execute('''
    SELECT schedule.Token, schedule.OT
    FROM schedule
    LEFT JOIN BoxScores ON schedule.Token = BoxScores.Token
    WHERE BoxScores.Token IS NULL AND schedule.Winner IS NOT NULL
''')
tokens = cursor.fetchall()



cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS BoxScores (
        boxscores_id INTEGER PRIMARY KEY,
        "BoxScore_ID" TEXT,
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
        "+/-" TEXT,
        "BoxScore_Type" TEXT,
        "Token" TEXT
        
    )
''')

conn.commit()

for t in tokens:
    tok = t[0]
    

    box_df = pd.read_csv(f"/Users/roy/Desktop/SPIDE/Phase2/csvs/BoxScores/{tok}.csv",header=None,skiprows= 1)
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
    
    if t[1] == "OT":
        header_titles=["G","Q1","Q2","H1","Q3","Q4","H2","OT","AG"]
    elif t[1] == "2OT":
        header_titles=["G","Q1","Q2","H1","Q3","Q4","H2","OT1","OT2","AG"]
    else:
        header_titles=["G","Q1","Q2","H1","Q3","Q4","H2","AG"]

    ind=0
    flag=away
    # Iterate through rows
    for index, row in box_df.iterrows():
        
        if type(row[1]) != float and 'Basic Box Score Stats' in row[1]:
            # If a new header is found, save the current dataframe (if any)
            # and create a new one with the new header
            if current_header is not None:
                dataframes[current_header] = current_dataframe
            if ind==len(header_titles):
                ind = 0
                flag = home 
            current_header = header_titles[ind]+" "+flag
            
            ind+=1
            current_dataframe = pd.DataFrame(columns=box_df.columns)
            # Append the current row to the current dataframe
        elif type(row[1]) != float and 'Advanced Box Score Stats' in row[1]:
            if current_header is not None:
                dataframes[current_header] = current_dataframe
            current_header = header_titles[ind]+" "+flag 
            ind+=1
            current_dataframe = pd.DataFrame(columns=box_df.columns)
            
        else:    
            current_dataframe = current_dataframe._append(pd.Series(row, index=box_df.columns), ignore_index=True)
            
    # Save the last dataframe
    if current_header is not None:
        if current_header not in dataframes:
            dataframes[current_header] = current_dataframe
        
    keys_to_delete = [key for key in dataframes.keys() if 'AG' in key]

    for key in keys_to_delete:
        del dataframes[key]

    for k in dataframes:

        new_column_names = (dataframes[k].iloc[0]).tolist()
        new_column_names[0] = "Player"

        new_column_names.append("BoxScore_ID")
        new_column_names.append("BoxScore_Type")
        new_column_names.append("Token")
        mask = dataframes[k][2]!= 'FG'
        df = dataframes[k][mask]
        df["BoxScore_ID"] = tok+"_"+k
        df["BoxScore_Type"] = k[0] if k[0] == 'G' else k[:2]
        df["Token"] = tok
        df.rename(columns=dict(zip(df.columns, new_column_names)), inplace=True)
        
        df.to_sql(f'BoxScores', conn, if_exists='append', index=False)

conncect_db.close_database_connection(conn)


																			