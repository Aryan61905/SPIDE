import requests

from bs4 import BeautifulSoup
from csvWriter import csv_writer



def OverallTeamStats():
    
    url = "https://www.basketball-reference.com/leagues/NBA_2024.html"
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(str(page_content), 'html.parser')
        csv_writer(soup,"/Users/roy/Desktop/SPIDE/Phase2/csvs/TeamStats.csv",'w')
    else:
        print("Failed to retrieve the webpage.")

OverallTeamStats()

