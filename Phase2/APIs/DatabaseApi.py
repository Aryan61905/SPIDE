from conncect_db import connect_to_database

conn,cursor = connect_to_database("Main")

def getStatsbyPlayer(player,stats = '*'):
    
    cursor.execute(f"Select {stats} from Players where Player = '{player}'")
    return cursor.fetchall()

def getPlayerStatsbyTeam(team,stats = '*'):
    cursor.execute(f"Select {stats} from Players where TM = '{team}'")
    return cursor.fetchall()

def getBoxScore(boxscore_id):
    cursor.execute(f"Select {id} from BoxScores where BoxScore_ID = '{boxscore_id}'")
    return cursor.fetchall()

def getSchedule():
    cursor.execute(f"Select * from Schedule")
    return cursor.fetchall()


def getOrderedStats(order="DESC", stat="PTS", num = 5):
    cursor.execute(f"SELECT Player,{stat} FROM Players ORDER BY {stat} {order} LIMIT {num}")
    return cursor.fetchall()





            