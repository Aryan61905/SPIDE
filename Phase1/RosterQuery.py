import mysql.connector
import Database


cursor,connection = Database.ConnectDB()

def GetPlayer(player_id):
    if type(player_id[0]) == str:
        cursor.execute("SELECT * FROM PLAYERS where player_name = %s;",player_id)
    else:
        cursor.execute("SELECT * FROM PLAYERS where player_id = %s;",player_id)
    player = cursor.fetchall()
    return player

def GetTeam(team_id):
    if type(team_id[0]) == str:
        cursor.execute("SELECT * FROM TEAMS where team_name = %s;",team_id)
    else:
        cursor.execute("SELECT * FROM TEAMS where team_id = %s;",team_id)
    team = cursor.fetchall()
    return team

def GetPlayersByTeam(team_id):
    if type(team_id[0]) == str:
        cursor.execute("SELECT * FROM PLAYERS where team_name = %s;",team_id)
    else:
        cursor.execute("SELECT * FROM PLAYERS where team_id = %s;",team_id)
    players = cursor.fetchall()
    return players

def GetTeamByPlayer(player_id):
    if type(player_id[0]) == str:
        cursor.execute("SELECT team_name FROM PLAYERS where player_name = %s;",player_id)
    else:
        cursor.execute("SELECT team_name FROM PLAYERS where player_id = %s;",player_id)
    players = cursor.fetchall()
    return players

#print(GetPlayer(["KyrieIrving"]))
#print(GetTeam(["Mavericks"]))
#print(GetPlayersByTeam(["Warriors"]))
print(GetTeamByPlayer(["StephenCurry"]))

Database.DisconnectDB(cursor,connection)