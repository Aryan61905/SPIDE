import mysql.connector
from mysql.connector import errorcode
import RosterUpdateAPI


connection = mysql.connector.connect(
                host='127.0.0.1',  # Replace with your MySQL host address
                user='root',    # Replace with your MySQL username
                password='SPIDE2023' # Replace with your MySQL password
            )

cursor = connection.cursor()

database_name = 'SPIDE_LOCAL_DB'  # Replace with your desired database name


cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")


cursor.execute(f"USE {database_name}")


cursor.execute("DELETE FROM PLAYERS")
reset_id_query = "ALTER TABLE PLAYERS AUTO_INCREMENT = 1"
cursor.execute(reset_id_query)
cursor.execute("DELETE FROM TEAMS")
reset_id_query = "ALTER TABLE TEAMS AUTO_INCREMENT = 1"
cursor.execute(reset_id_query)

create_table_query = """
        CREATE TABLE IF NOT EXISTS NBA (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_name VARCHAR(255) NOT NULL,
        )
    """
create_team_query =""" 
    CREATE TABLE IF NOT EXISTS TEAMS(
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL
);
"""
create_player_query = """
    CREATE TABLE IF NOT EXISTS PLAYERS(
        player_id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(100) NOT NULL,
        team_id INT,
        team_name VARCHAR(100),
        FOREIGN KEY (team_id) REFERENCES TEAMS(team_id)
);
"""
cursor.execute(create_team_query)
cursor.execute(create_player_query)
TeamMap={}
TeamMap = RosterUpdateAPI.RosterUpdate()

teams = TeamMap.keys()
insert_team_query = "INSERT INTO TEAMS (team_name) VALUES (%s)"
teams = list(TeamMap.keys())
team_values = [(team,) for team in teams]
cursor.executemany(insert_team_query, team_values)

# 4. Insert players into the "Players" table and associate them with their respective teams
insert_player_query = "INSERT INTO Players (player_name, team_id,team_name) VALUES (%s, %s,%s)"
for team_name, players in TeamMap.items():
    team_id_query = "SELECT team_id FROM TEAMS WHERE team_name = %s"
    cursor.execute(team_id_query, (team_name,))
    team_id = cursor.fetchone()[0]
    player_values = [(player, team_id,team_name) for player in players]
    cursor.executemany(insert_player_query, player_values)

cursor.execute("SELECT * FROM PLAYERS;")
rows= cursor.fetchall()
print(rows)

connection.commit()
cursor.close()
connection.close()

