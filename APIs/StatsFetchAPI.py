import requests
import time
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from RosterQuery import GetPlayer, GetPlayersByTeam, GetTeamByPlayer, GetTeam

TierMap2={}

stats_url = "https://www.nba.com/stats/players/traditional?SeasonType=Regular+Season"
driver = webdriver.Safari()
driver.get(stats_url)
time.sleep(0.9)
button = driver.find_element(By.CLASS_NAME, 'ArrowToggleButton_arrowButton__9RpIv')
button.click()
