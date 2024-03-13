import DatabaseApi
import Parser
from conncect_db import connect_to_database, close_database_connection




def main(input,conn,cursor):

    player_data_dict={}
    ret_app=[]
    data_dict = Parser.parse_input(input)

    #print(data_dict)
    
    def getTeams():
        teams = DatabaseApi.getList(conn,cursor,'Tm','Players')[0]
        mod_teams=[]
        for team in teams:
            mod_teams.append(team[0])
        return mod_teams
    
    def populatePlayers():
        for player_key in data_dict['player']:
            
            teams = getTeams()
            
            if player_key in teams:
                
                players= DatabaseApi.getStats(conn,cursor,'Player','Players','Tm',player_key)[0]
                for p in players:
                    data_dict["player"].append(p[-1])
        
        data_dict['player'] = [val for val in data_dict['player'] if val not in teams]

        for player_key in data_dict['filter']['Player']:
            if player_key[1:] in teams:
                data_dict['filter']['Team'].append(player_key)
         
        data_dict['filter']['Player'] = [val for val in data_dict['filter']['Player'] if val[1:] not in teams]        

    def getStatsByDateRange(sd,ed):
        ret=[]     
        result={}
        sd = (sd.replace('/',""))
        ed= (ed.replace('/',""))
        sd = (sd[4:8]+sd[0:2]+sd[2:4])
        ed = (ed[4:8]+ed[0:2]+ed[2:4])
        
        for player_key in data_dict["player"]:
        
            for gt in data_dict['filter']['GameType']:
                special = {'AVG':{},'SUM':{}}
                copy_stats = data_dict['stats'][:]
                for i in data_dict['stats']:
                    if '(' in i and i[:i.index('(')] in special.keys():
                        special[i[:i.index('(')]][i[i.index('(')+1:i.index(')')]]=0
                        data_dict['stats'][data_dict['stats'].index(i)]= i[i.index('(')+1:i.index(')')]
                    
                select_v = ', '.join(['\"{}\"'.format(item) if item[0].isdigit() else '{}'.format(item) for item in data_dict['stats']])
                select_v += ', Opponent'
                db_data  = DatabaseApi.getBoxScoreStatsByDateRange(conn,cursor,select_v,'BoxScores',['Player','BoxScore_Type'],[player_key,gt],sd,ed,'DESC' if ed<sd else 'ASC')
                num = len(db_data[0])-1
                i=0
                av = 0
                
                while i<=num:
                    
                    player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][i]))
                    result[player_key+" VS "+player_data_dict[player_key]["Opponent"]+" on " + player_data_dict[player_key]["Date"][4:6]+"/"+player_data_dict[player_key]["Date"][6:8]+"/"+player_data_dict[player_key]["Date"][0:4]] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
                    if db_data[0][i][0] == None:
                        i=i+1
                        av+=1
                        continue
                    for st in db_data[1]:
                        for y in special:
                            if st in special[y]:
                                special[y][st]+=player_data_dict[player_key][st]              

                    i=i+1
                
                for st in special['AVG']:
                    
                    special["AVG"][st]/= int(len(result.keys())) - av
                
                if num >=0:
                    if sd!=ed:
                        ret.append(Parser.parse_output(result,player_key,gt,dr[0]+"->"+dr[1]))
                        ret.append(Parser.parse_output_special(special,player_key,gt,dr[0]+"->"+dr[1]))
                    else:
                        ret.append(Parser.parse_output(result,player_key,gt,sd))
                        ret.append(Parser.parse_output_special(special,player_key,gt,sd))

                    result={}
                    data_dict['stats']=copy_stats
        if ret!=[]:
            return ret

    def getAvgStats(gt="G"):
        result={}
        ret=[]
        for player_key in data_dict['player']:

            #db_data = DatabaseApi.getStats('*','Players','player',player_key)
            
            
            select_v = ', '.join(['AVG(\"{}\")'.format(item) if item[0].isdigit() else 'AVG({})'.format(item) for item in data_dict['stats']])
            

            db_data  = DatabaseApi.getBoxScoreStats(conn,cursor,select_v,'BoxScores',['Player','BoxScore_Type'], [player_key,gt],None,'AVG') 
            player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][0]))
            result[player_key]  = player_data_dict[player_key]
            #result[player_key] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
            ret.append(Parser.parse_output(result,player_key,'OVR','AVG'))
            result={}
            
        
        if ret!=[]:
            return ret
            

    def getXGames(x):
        
        result={}
        ret=[]
        for player_key in data_dict["player"]:
            
            for gt in data_dict['filter']['GameType']:
                special = {'AVG':{},'SUM':{}}
                copy_stats = data_dict['stats'][:]
                for i in data_dict['stats']:
                    if '(' in i and i[:i.index('(')] in special.keys():
                        special[i[:i.index('(')]][i[i.index('(')+1:i.index(')')]]=0
                        data_dict['stats'][data_dict['stats'].index(i)]= i[i.index('(')+1:i.index(')')]
                    
                select_v = ', '.join(['\"{}\"'.format(item) if item[0].isdigit() else '{}'.format(item) for item in data_dict['stats']])
                select_v += ', Opponent,Token'
                num = int(x[1:])-1
                db_data  = DatabaseApi.getBoxScoreStats(conn,cursor,select_v,'BoxScores',['Player','BoxScore_Type'], [player_key,gt],num,'DESC' if x[0]=='L' else 'ASC')
                c_db_data =db_data[:]
                if data_dict['filter']['Player'] or data_dict['filter']['Team']:

                    for op_player in data_dict['filter']['Player']:
                        
                        copy_stats = data_dict['stats'][:]
                        num = int(x[1:])-1
                        if op_player[0]=='+':
                            select_v = 'PTS,Player,Opponent,MP,PTS,Date,Token'
                            
                            op_db_data = DatabaseApi.getBoxScoreStats(conn,cursor,select_v,'BoxScores',['Player','BoxScore_Type'], [op_player[1:],gt],num,'DESC')
                            tokens = [tok[-1] for tok in op_db_data[0]]
                            db_data[0] = [vals for vals in db_data[0] if vals[-1] in tokens and vals[0]!= None]

                        if num >len(db_data[0])-1:
                            num = len(db_data[0])-1
                        i=0
                        av = 0
                        while i<=num:
                            
                            player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][i]))
                            result[player_key+" VS "+player_data_dict[player_key]["Opponent"]+" "+op_player+" "+" "+x[0]+str(i+1)] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
                            if db_data[0][i][0] == None:
                                i=i+1
                                av+=1
                                continue
                            for st in db_data[1]:
                                for y in special:
                                    if st in special[y]:
                                        special[y][st]+=player_data_dict[player_key][st]              

                            i=i+1
                        
                        
                        for st in special['AVG']:
                                special["AVG"][st]/= len(db_data[0]) - av
                        
                        ret.append(Parser.parse_output(result,player_key,gt,x))
                        ret.append(Parser.parse_output_special(special,player_key,gt,x))
                        result={}
                        for st in db_data[1]:
                            for y in special:
                                if st in special[y]:
                                    special[y][st]=0
                        

                
                    for op_team in data_dict['filter']['Team']:
                       
                        
                        
                        copy_stats = data_dict['stats'][:]
                        db_data = c_db_data[:]
                        num = int(x[1:])-1
                        if op_team[0]=='+':
                            
                            op_db_data  = DatabaseApi.getBoxScoreStats(conn,cursor,select_v,'BoxScores',['Player','BoxScore_Type','Opponent'], [player_key,gt,op_team[1:]],num,'DESC' if x[0]=='L' else 'ASC')
                            tokens = [tok[-1] for tok in op_db_data[0]]
                            db_data[0] = [vals for vals in db_data[0] if vals[-1] in tokens and vals[0]!= None]
                        if num >len(db_data[0])-1:
                            num = len(db_data[0])-1
                        i=0
                        av = 0
                        while i<=num:
                            
                            player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][i]))
                            result[player_key+" VS "+player_data_dict[player_key]["Opponent"]+" "+x[0]+str(i+1)] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
                            if db_data[0][i][0] == None:
                                i=i+1
                                av+=1
                                continue
                            for st in db_data[1]:
                                for y in special:
                                    if st in special[y]:
                                        special[y][st]+=player_data_dict[player_key][st]              

                            i=i+1
                        
                        
                        for st in special['AVG']:
                                special["AVG"][st]/= len(db_data[0]) - av
                        
                        ret.append(Parser.parse_output(result,player_key,gt,x))
                        ret.append(Parser.parse_output_special(special,player_key,gt,x))
                        result={}
                        for st in db_data[1]:
                            for y in special:
                                if st in special[y]:
                                    special[y][st]=0
                        
                        
                
                else:
                    
                    
                    if num >len(db_data[0])-1:
                        num = len(db_data[0])-1
                    i=0
                    av = 0
                    while i<=num:
                        
                        player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][i]))
                        result[player_key+" VS "+player_data_dict[player_key]["Opponent"]+" "+x[0]+str(i+1)] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
                        if db_data[0][i][0] == None:
                            i=i+1
                            av+=1
                            continue
                        for st in db_data[1]:
                            for y in special:
                                if st in special[y]:
                                    special[y][st]+=player_data_dict[player_key][st]              

                        i=i+1
                    
                    
                    for st in special['AVG']:
                            special["AVG"][st]/= int(x[1:]) - av
                    
                    ret.append(Parser.parse_output(result,player_key,gt,x))
                    ret.append(Parser.parse_output_special(special,player_key,gt,x))
                    result={}
                    
                    data_dict['stats']=copy_stats

        if ret!=[]:
            return ret
        
        

    populatePlayers()

 
    if data_dict["filter"]=={
                      'GameType':[],
                      'XGames':[],
                      'DateRange':[],
                      'Date':[],
                      'PlayerOrTeam':[]
                  }:
        ret_app.append(getAvgStats())
        
    elif data_dict["filter"]['GameType']!=[] and data_dict["filter"]['XGames'] == [] and data_dict["filter"]['DateRange']==[] and data_dict["filter"]['Date'] == [] and data_dict["filter"]['PlayerOrTeam']==[]:
        for gt in data_dict["filter"]['GameType']:
            ret_app.append(getAvgStats(gt))
        
    
    for x in data_dict['filter']['XGames']:
        ret_app.append(getXGames(x))
        

    for dr in data_dict['filter']["DateRange"]:
        
        dr = dr.split('->')
        sd = dr[0]
        ed = dr[1]
        ret_app.append(getStatsByDateRange(sd,ed))
    
    for dr in data_dict['filter']["Date"]:
        
        sd = dr
        ed = dr
        ret_app.append(getStatsByDateRange(sd,ed))

    

    for schedule_key in data_dict["schedule"]:
        pass 

   #print(player_data_dict)

    return ret_app

#main("--player Joel Embiid, Luka Dončić, Giannis Antetokounmpo, Kevin Durant, Domantas Sabonis, Devin Booker, Jayson Tatum, Donovan Mitchell, LaMelo Ball, De'Aaron Fox, Damian Lillard --stats PTS,TRB,AST,boxscores_id,Token,Date --filter L5")
#main("--player Nikola Jokić,Julius Randle, Jalen Brunson,Shai Gilgeous-Alexander,Anthony Davis, Kawhi Leonard,LeBron James --stats PTS,TRB,AST,boxscores_id,Token,Date --filter L10,G")
#main("--player Devin Booker --stats 3P,3PA,boxscores_id,Token,Date --filter L6,H1, 01/10/2024->01/16/2024")
#main("--player  Kevin Durant,Devin Booker,Anthony Davis,Domantas Sabonis,Giannis Antetokounmpo,Jayson Tatum,LeBron James, Stephen Curry, Jalen Brunson, Joel Embiid, Tyrese Haliburton --stats AVG(PTS),AVG(AST),AVG(TRB),AVG(PTS+TRB+AST>45),Date --filter L8,G")
#conn,cursor= connect_to_database('Main')
#main("--player Joel Embiid,Paul George,Jayson Tatum,Stephen Curry, Trae Young,Donovan Mitchell,Domantas Sabonis   --stats PTS,TRB,AST, AVG(PTS+TRB+AST),Date,MP --filter 01/01/2024->02/01/2024,G",conn,cursor)
#main_ret
