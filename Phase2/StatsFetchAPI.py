import requests

from bs4 import BeautifulSoup
from csvWriter import csv_writer
import pandas as pd


def OverallPlayerStats():
    
    url = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.text
        soup = BeautifulSoup(str(page_content), 'html.parser')
        csv_writer(soup,"OverallPlayerStats.csv",'w')
    else:
        print("Failed to retrieve the webpage.")

OverallPlayerStats()




