import requests

from bs4 import BeautifulSoup
from csvWriter import csv_writer

import pandas as pd




def Schedule():
    
    for month in ["october","november","december","january","february","march","april"]:
        url = f"https://www.basketball-reference.com/leagues/NBA_2024_games-{month}.html"
        response = requests.get(url)

        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(str(page_content), 'html.parser')
            csv_writer(soup,"Schedule.csv",'a')
        else:
            print("Failed to retrieve the webpage.")

Schedule()




