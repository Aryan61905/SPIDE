import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


team_url = 'https://www.nba.com/teams'
Tier1Map = {}

response_team = requests.get(team_url)


if response_team.status_code == 200:
   
    soup_team = BeautifulSoup(response_team.content, 'html.parser')
    team_elements = soup_team.find_all('span', attrs = {'class':'NavTeamList_ntlName__Mzr6q' })
    
    
    teams = [team.get_text() for team in team_elements]
    
    # Print the list of team names
    for t in range(len(teams)):
        
      
        teams[t] = teams[t][teams[t].index(" ")+1:]
        
        
        #print(teams[t])
    
player_url ='https://www.nba.com/players'
#response_player = requests.get(player_url)
driver = webdriver.Safari()
driver.get(player_url)
time.sleep(0.5)
select = Select(driver.find_element("name","TEAM_NAME"))

for team in teams:
    #print('/n')
    #print(team)
    while True:
        try: 
            select.select_by_value(str(team))
            Tier1Map[team]=[]
            break
        except NoSuchElementException:
            t_team = team[team.index(" ")+1:]
            select.select_by_value(str(t_team))
            Tier1Map[t_team]=[]
            break

    response_player = driver.page_source

    soup_player = BeautifulSoup(response_player, 'html.parser')
    #print(soup_player)
    player_elements = soup_player.find_all('div',attrs = {"class":"RosterRow_playerName__G28lg"})
    #print(player_elements)
    players = [player.get_text() for player in player_elements]
    #print(players)
    for player in players:
        try:
            Tier1Map[team].append(player)
        except KeyError:
            Tier1Map[t_team].append(player)

        #print((player))
#print(Tier1Map)
for team in Tier1Map.keys():
    print(team,Tier1Map[team])
    

