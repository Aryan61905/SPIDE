
import conncect_db
import pandas as pd
import numpy as np
# Create a new SQLite database or connect to an existing one
conn,cursor = conncect_db.connect_to_database("Main")


# Read the CSV data
df = pd.read_csv("/Users/roy/Desktop/SPIDE/Phase2/csvs/Schedule.csv")
df = df[df.Date != "Date"]
months= {
    "Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"
}

token_dict = {
    "GOL":"GSW", "SAN": "SAS", "BRO": "BRK", "CHA": "CHO", "CLIPPERS":"LAC", "LAKERS":"LAL", "NEW":"NOP", "PELICANS": "NOP", "KNICKS": "NYK", "OKL": "OKC"
}




def modify_token(value):
    team_chars = value[0:3].upper()
    if team_chars in ["NEW", "LOS"]: 
        team_chars = token_dict[value.split(" ")[-1].upper()]
    elif team_chars in token_dict:
        team_chars = token_dict[team_chars]
    
    return team_chars

df["Home_Token"] = df["Home/Neutral"].apply(modify_token)
df["Visitor_Token"] = df["Visitor/Neutral"].apply(modify_token)
df['Token'] = df['Date'].apply(lambda x: f"{x[-4:]}{months[x.split(',')[1][1:4]]}{x.split(',')[1][5:7].zfill(2)}")+"0"+df["Home_Token"]+"VS"+df["Visitor_Token"]

# Insert the data into the Players table

df["PTS"] = pd.to_numeric(df["PTS"], errors='coerce').astype(float)

df["PTS.1"] = pd.to_numeric(df["PTS.1"], errors='coerce').astype(float)

new_column_names=["Date",'Start (ET)', 'Away', 'Away_PTS', 'Home', 'Home_PTS', 'Winner', 'OT',"Attendance", "Arena", "Game_Type","Home_Token","Visitor_Token","Token"]

df.rename(columns=dict(zip(df.columns, new_column_names)), inplace=True)

df["Winner"] = np.where(df['Home_PTS'].notna() & df['Away_PTS'].notna(),
                        np.where(df['Home_PTS'] > df['Away_PTS'], df['Home'], df['Away']),
                        np.nan)


df.to_sql('Schedule', conn, if_exists='replace', index=True)


conncect_db.close_database_connection(conn)