from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import time
import mysql.connector
try:
    connection = mysql.connector.connect(
        user="root",
        password="*******",
        host="localhost",
        port=3306,
        database="soccer",
        use_unicode=True, 
        charset="utf8mb3"

    )
except:
    print("Error Connection to sql")
    #print(f"Error connecting to Mysql Platform: {e}")
    pass
    
cursor=connection.cursor()
command="""CREATE TABLE IF NOT EXISTS stats(Team LONGTEXT, Matches_played LONGTEXT, Wins LONGTEXT, Losses LONGTEXT, Goals LONGTEXT, Goals_Conceded LONGTEXT, Clean_sheets LONGTEXT, shot_accuracy LONGTEXT, pass_accuracy LONGTEXT, tackle_success LONGTEXT, error_leading_to_goals LONGTEXT, own_goals LONGTEXT) DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"""
cursor.execute(command) 

#driver=webdriver.Chrome('C:/Users/mkolla1/Downloads/chromedriver')
driver = webdriver.Chrome(executable_path='/home/ebcs/Desktop/EBCS-Darknet/chromedriver')
driver.get("https://www.premierleague.com/stats/top/clubs/wins")
time.sleep(5)
team_main_links=[]
team_main_links_elements=driver.find_element(By.CLASS_NAME, "statsTableContainer").find_elements(By.CLASS_NAME, "table__row")
for main_link in team_main_links_elements:
    team_main_links.append(main_link.find_element(By.CLASS_NAME, "stats-table__name").find_element(By.TAG_NAME,"a").get_attribute("href"))
club_stat_links=[]
for club in team_main_links:
    link=club.replace("overview", "stats")
    club_stat_links.append(link)

links=["https://www.premierleague.com/clubs/6/club/stats","https://www.premierleague.com/clubs/34/club/stats","https://www.premierleague.com/clubs/7/club/stats","https://www.premierleague.com/clubs/15/club/stats","https://www.premierleague.com/clubs/38/club/stats","https://www.premierleague.com/clubs/130/club/stats","https://www.premierleague.com/clubs/43/club/stats","https://www.premierleague.com/clubs/163/club/stats"]
club_stat_links+=links
for stats in club_stat_links:
    driver.get(stats)
    time.sleep(2)
    names=[]
    values=[]
    team_name=driver.find_element(By.CLASS_NAME, "club-header__team-name").text
    values.append(team_name)
    top_6_elements=driver.find_element(By.CLASS_NAME, "all-stats__top-list").find_elements(By.CLASS_NAME, "all-stats__top-stat-container")
    for i in top_6_elements:
        #print(i.find_element(By.CLASS_NAME, "all-stats__top-stat-name").text, ":",i.find_element(By.CLASS_NAME, "all-stats__top-stat").text )
        names.append(i.find_element(By.CLASS_NAME, "all-stats__top-stat-name").text)
        values.append(i.find_element(By.CLASS_NAME, "all-stats__top-stat").text)


    values.append(driver.find_element(By.CLASS_NAME, "statshot_accuracy").text)
    values.append(driver.find_element(By.CLASS_NAME, "statpass_accuracy").text)
    values.append(driver.find_element(By.CLASS_NAME, "stattackle_success").text)
    values.append(driver.find_element(By.CLASS_NAME, "staterror_lead_to_goal").text)
    values.append(driver.find_element(By.CLASS_NAME, "statown_goals").text)
    
    cursor.execute("INSERT INTO stats(Team, Matches_played, Wins, Losses, Goals, Goals_Conceded, Clean_sheets, shot_accuracy, pass_accuracy, tackle_success, error_leading_to_goals, own_goals) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9],values[10],values[11]))
    connection.commit()
    print("######Data Inserted Successfully##################")
