import sqlite3
from WebScrappers.PlayerStatsFetch import PlayerStatsFetch
from WebScrappers.ScheduleFetch import ScheduleFetch
from WebScrappers.BoxScoreFetch import BoxScoreFetch
from WebScrappers.PlaybyPlayFetch import PlayByPlayFetch
db_ids= {
    'Main':'/Users/roy/Desktop/SPIDE/Phase3/Database/NBA_db.db',
    }
def connect_db(db_id):
    conn = sqlite3.connect(db_ids[db_id])
    cursor = conn.cursor()
    return conn, cursor

def disconnect_db(conn):
    conn.commit()
    conn.close()

def PlayersTableReset():
    createPlayersTable = '''
    CREATE TABLE PLAYERS(  
    PlayerId INTEGER PRIMARY KEY AUTOINCREMENT,
    Rk INT,  
    Player VARCHAR(150), 
    Age INT,  
    Team VARCHAR(50),  
    Pos VARCHAR(3),  
    G INT,  
    GS INT, 
    MP DOUBLE,  
    FG DOUBLE,  
    FGA DOUBLE,  
    "FG%" DOUBLE,  
    "3P" DOUBLE,  
    "3PA" DOUBLE,  
    "3P%" DOUBLE,  
    "2P" DOUBLE,  
    "2PA" DOUBLE,  
    "2P%" DOUBLE,  
    "eFG%" DOUBLE,  
    FT DOUBLE,  
    FTA DOUBLE,  
    "FT%" DOUBLE,  
    ORB DOUBLE,  
    DRB DOUBLE,  
    TRB DOUBLE,  
    AST DOUBLE,  
    STL DOUBLE,  
    BLK DOUBLE,  
    TOV DOUBLE,  
    PF DOUBLE,  
    PTS DOUBLE,  
    Awards VARCHAR(255)); 
    '''

    conn,cursor = connect_db("Main")
    cursor.execute('DROP TABLE IF EXISTS PLAYERS')
    cursor.execute(createPlayersTable)
    disconnect_db(conn)

def PlayersTableUpdate():
    PlayersTableReset()
    player_data = PlayerStatsFetch()[1:-1]
    player_val = ''
    for pd in player_data:
        player_val+= f"(null,{str(pd)[1:-1]}), "

    updatePlayersTable = f'''
    INSERT INTO PLAYERS (PlayerId, Rk, Player, Age, Team, Pos, G, GS, MP, FG, FGA, `FG%`, `3P`, `3PA`, `3P%`, `2P`, `2PA`, `2P%`, `eFG%`, FT, FTA, `FT%`, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, Awards)
    VALUES {player_val[:-2]};'''
    conn,cursor = connect_db("Main")
    cursor.execute(updatePlayersTable)
    disconnect_db(conn)

def ScheduleTableReset():
    createScheduleTable = '''
    CREATE TABLE SCHEDULE( 
    ScheduleId INTEGER PRIMARY KEY AUTOINCREMENT, 
    Date VARCHAR(10), 
    StartTime VARCHAR(5), 
    AwayTeam VARCHAR(3), 
    AwayTeamPTS INT, 
    HomeTeam VARCHAR(3), 
    HomeTeamPTS INT, 
    BoxScoreId VARCHAR(100), 
    OverTime VARCHAR(3), 
    Attendence VARCHAR(6), 
    LengthOfGame VARCHAR(4), 
    Arena VARCHAR(50), 
    Notes VARCHAR(100)
    ); 
    '''

    conn,cursor = connect_db("Main")
    cursor.execute('DROP TABLE IF EXISTS SCHEDULE')
    cursor.execute(createScheduleTable)
    disconnect_db(conn)

def ScheduleTableUpdate():
    ScheduleTableReset()
    schedule_data = ScheduleFetch()
    schedule_val = ''
    for sd in schedule_data:
        schedule_val+= f"(null,{str(sd)[1:-1]}), "

    updateScheduleTable = f'''
    INSERT INTO SCHEDULE (ScheduleId, Date, StartTime, AwayTeam, AwayTeamPTS, HomeTeam, HomeTeamPTS, BoxScoreId, OverTime, Attendence, LengthOfGame, Arena, Notes)
    VALUES {schedule_val[:-2]};'''
    conn,cursor = connect_db("Main")
    cursor.execute(updateScheduleTable)
    disconnect_db(conn)

def BoxScoreTableReset():

    createBoxScoreBasicTable = '''
    CREATE TABLE BOXSCOREBASIC( 
    BoxScoreID INTEGER PRIMARY KEY AUTOINCREMENT, 
    Player VARCHAR(150), 
    MP VARCHAR(5), 
    FG INTEGER, 
    FGA INTEGER, 
    "FG%" DOUBLE, 
    "3P" INTEGER, 
    "3PA" INTEGER, 
    "3P%" DOUBLE, 
    FT INTEGER,  
    FTA INTEGER, 
    "FT%" DOUBLE, 
    ORB INTEGER, 
    DRB INTEGER, 
    TRB INTEGER, 
    AST INTEGER, 
    STL INTEGER, 
    BLK INTEGER, 
    TOV INTEGER, 
    PF INTEGER, 
    PTS INTEGER, 
    GmSc DOUBLE, 
    "+/-" INTEGER,
    BenchStatus VARCHAR(1),
    Team VARCHAR(3),
    Opponent VARCHAR(3),
    Type VARCHAR(4),
    Token VARCHAR(12)
    ); 
    '''

    createBoxScoreAdvancedTable = '''
    CREATE TABLE BOXSCOREADVANCED( 
    BoxScoreID INTEGER PRIMARY KEY AUTOINCREMENT, 
    Player VARCHAR(150), 
    MP VARCHAR(5), 
    "TS%" DOUBLE, 
    "eFG%" DOUBLE, 
    "3PAr" DOUBLE, 
    FTr DOUBLE, 
    "ORB%" DOUBLE, 
    "DRB%" DOUBLE, 
    "TRB%" DOUBLE, 
    "AST%" DOUBLE, 
    "STL%" DOUBLE, 
    "BLK%" DOUBLE, 
    "TOV%" DOUBLE, 
    "USG%" DOUBLE, 
    ORtg DOUBLE, 
    DRtg DOUBLE, 
    BPM DOUBLE,
    BenchStatus VARCHAR(1),
    Team VARCHAR(3),
    Opponent VARCHAR(3),
    Type VARCHAR(4),
    Token VARCHAR(12)
   ); 
    '''

    conn,cursor = connect_db("Main")
    cursor.execute('DROP TABLE IF EXISTS BOXSCOREBASIC')
    cursor.execute(createBoxScoreBasicTable)
    cursor.execute('DROP TABLE IF EXISTS BOXSCOREADVANCED')
    cursor.execute(createBoxScoreAdvancedTable)
    disconnect_db(conn)
   
def BoxScoreTableUpdate():
    #BoxScoreTableReset()
    conn,cursor = connect_db("Main")
    cursor.execute('SELECT BoxScoreId from SCHEDULE where HomeTeamPTS')
    BoxscoreIds = [i[0] for i in cursor.fetchall()[0:5]]
    cursor.execute('SELECT DISTINCT TOKEN from BOXSCOREBASIC')
    BoxscoreBasicTokens = [i[0] for i in cursor.fetchall()]
    cursor.execute('SELECT DISTINCT TOKEN from BOXSCOREADVANCED')
    BoxscoreAdvancedTokens = [i[0] for i in cursor.fetchall()]
    
    for path in BoxscoreIds:
        if path[-17:-5] in BoxscoreAdvancedTokens and path[-17:-5] in BoxscoreBasicTokens:
            print(path[-17:-5],"Already in both BOXSCORE Tables")
            continue

        BoxScoredata = BoxScoreFetch(path)
        if type(BoxScoredata) != dict:
            print(f"Error fetching Boxscore path: {path} \n ErrorCode: {BoxScoredata}")
        else:
            for key in BoxScoredata:
                boxscore_val = ''
                for bd in BoxScoredata[key]:
                    boxscore_val+= f"(null,{str(bd)[1:-1]}), "

                if key[key.rindex('-')+1:] == 'basic':
                    updateBoxScoreTable = f'''
                    INSERT INTO BOXSCOREBASIC (BoxScoreID, Player, MP, FG, FGA, `FG%`, `3P`, `3PA`, `3P%`, FT, FTA, `FT%`, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, GmSc, `+/-`, BenchStatus, Team, Opponent, Type, Token)
                    VALUES {boxscore_val[:-2]};'''
                    if path[-17:-5] not in BoxscoreBasicTokens:
                        cursor.execute(updateBoxScoreTable)
                    else:
                        print(path[-17:-5],"Already in Database BOXSCOREBASIC")
                else :
                    updateBoxScoreTable = f'''
                    INSERT INTO BOXSCOREADVANCED (BoxScoreID, Player, MP, `TS%`, `eFG%`, `3PAr`, FTr, `ORB%`, `DRB%`, `TRB%`, `AST%`, `STL%`, `BLK%`, `TOV%`, `USG%`, ORtg, DRtg, BPM, BenchStatus, Team, Opponent, Type, Token)
                    VALUES {boxscore_val[:-2]};'''
                    if path[-17:-5] not in BoxscoreAdvancedTokens:
                        cursor.execute(updateBoxScoreTable)
                    else:
                        print(path[-17:-5],"Already in Database BOXSCOREADVANCED")

    disconnect_db(conn)

def PlayByPlayReset():
    createPlayByPlayTable = '''
    CREATE TABLE PLAYBYPLAY( 
    PlayByPlayID INTEGER PRIMARY KEY AUTOINCREMENT, 
    Quarter VARCHAR(6),
    Time VARCHAR(10),
    AwayTeamPlay VARCHAR(255),
    AwayTeamScoreDiff VARCHAR(5),
    Score VARCHAR(10),
    HomeTeamPlay VARCHAR(255),
    HomeTeamScoreDiff VARCHAR(5),
    Token VARCHAR(12)
   ); 
    '''
    conn,cursor = connect_db("Main")
    cursor.execute('DROP TABLE IF EXISTS PLAYBYPLAY')
    cursor.execute(createPlayByPlayTable)
    disconnect_db(conn)

def PlayByPlayUpdate():

    conn,cursor = connect_db("Main")
    cursor.execute('SELECT BoxScoreId from SCHEDULE where HomeTeamPTS')
    BoxscoreIds = [i[0] for i in cursor.fetchall()[0:5]]
    cursor.execute('SELECT DISTINCT TOKEN from PLAYBYPLAY')
    PlayByPlayTokens = [i[0] for i in cursor.fetchall()]

    for path in BoxscoreIds:
        if path[-17:-5] in PlayByPlayTokens: 
            print(path[-17:-5],"Already in both PLAYBYPLAY Table")
            continue

        PlayByPlaydata = PlayByPlayFetch(path[-17:-5])
        if type(PlayByPlaydata) != list:
            print(f"Error fetching Boxscore path: {path} \n ErrorCode: {PlayByPlaydata}")
        else:
            
                playbyplay_val = ''
                for pd in PlayByPlaydata:
                    playbyplay_val += f"(null,{str(pd)[1:-1]}), "

                updatePlayByPlayTable = f'''
                INSERT INTO PLAYBYPLAY (PlayByPlayID, Quarter, Time, AwayTeamPlay, AwayTeamScoreDiff, Score, HomeTeamPlay, HomeTeamScoreDiff, Token)
                VALUES  {playbyplay_val[:-2]};'''
                if path[-17:-5] not in PlayByPlayTokens:
                    cursor.execute(updatePlayByPlayTable)
                else:
                    print(path[-17:-5],"Already in Database PLAYBYPLAY")

    disconnect_db(conn)

#PlayersTableUpdate()
#ScheduleTableUpdate()
#BoxScoreTableReset()
#BoxScoreTableUpdate()
#PlayByPlayReset()
PlayByPlayUpdate()
