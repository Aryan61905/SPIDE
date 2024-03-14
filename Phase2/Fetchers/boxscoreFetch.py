import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
from csvWriter import csv_writer
import time


# Start_Date : MM/DD/YYYY
# End_Date : MM/DD/YYYY

def boxScore(Start_date, End_date):

    Start_date = Start_date.split('/')
    End_date = End_date.split('/')

    df = pd.read_csv("/Users/roy/Desktop/SPIDE/Phase2/csvs/Schedule.csv")

    df = df[df.Date != "Date"]

    months = {
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
    df['Token'] = df['Date'].apply(lambda x: f"{x[-4:]}{months[x.split(',')[1][1:4]]}{x.split(',')[1][5:7].zfill(2)}")+"0"+df["Home_Token"]

    df = df[(df['Token'].str[4:6].astype(int) >= int(Start_date[0])) & (df['Token'].str[4:6].astype(int) <= int(End_date[0])) & (df['Token'].str[6:8].astype(int) >= int(Start_date[1])) &(df['Token'].str[6:8].astype(int) <= int(End_date[1]))]

    selected_columns = ["Token", "Visitor_Token"]

    df = df[selected_columns]

    for index, row in df.iterrows():
        print(f"Row {index}: {row['Token']}, {row['Visitor_Token']}")

        token = str(row['Token'])
        visitor = str(row['Visitor_Token'])   
        visitor=visitor.split()[0].upper()
        
            
        time.sleep(5)
        url = f"https://www.basketball-reference.com/boxscores/{token}.html"
        response = requests.get(url)

        path = f"/Users/roy/Desktop/SPIDE/Phase2/csvs/BoxScores/{token}VS{visitor}.csv"
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(str(page_content), 'html.parser')

            csv_writer(soup,path,'a')
        else:
            print("Failed to retrieve the webpage.")

boxScore("03/13/2024","03/13/2024")