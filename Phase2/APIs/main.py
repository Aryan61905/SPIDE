import DatabaseApi
import Parser




def main(input):

    player_data_dict={}
    result={}
    data_dict = Parser.parse_input(input)
    #print(data_dict)
    
    
    
        

    def getTeams():
        teams = DatabaseApi.getList('Tm','Players')[0]
        mod_teams=[]
        for team in teams:
            mod_teams.append(team[0])
        return mod_teams

    for player_key in data_dict['player']:
        
        teams = getTeams()
        if player_key in teams:
            
            players= DatabaseApi.getStats('Player','Players','Tm',player_key)[0]
            for p in players:
                data_dict["player"].append(p[-1])
    
    data_dict['player'] = [val for val in data_dict['player'] if val not in teams]

    if data_dict["filter"]==[]:

        for player_key in data_dict['player']:

            db_data = DatabaseApi.getStats('*','Players','player',player_key)
            player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][0]))
            result[player_key] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
    
    else:
            
        for x in data_dict['filter']['XGames']:
        
            
            for player_key in data_dict["player"]:
                
                for gt in data_dict['filter']['GameType']:

                    db_data  = DatabaseApi.getBoxScoreStats('*','BoxScores',['Player','BoxScore_Type'], [player_key,gt],'DESC' if x[0]=='L' else 'ASC') 
                    
                    num = int(x[1:])-1
                    if num >len(db_data[0])-1:
                        num = len(db_data[0])-1
                    i=0
                    
                    
                    while i<=num:
                        
                        player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][i]))
                        result[player_key+" "+x[0]+str(i+1)] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
                        i=i+1
                    Parser.parse_output(result,player_key,gt,x)
                    result={}
        
        for dr in data_dict['filter']["DateRange"]:
            
            dr = dr.split('->')
            sd = dr[0]
            ed = dr[1]
            sd = (sd.replace('/',""))
            ed= (ed.replace('/',""))
            sd = (sd[4:8]+sd[0:2]+sd[2:4])
            ed = (ed[4:8]+ed[0:2]+ed[2:4])
            for player_key in data_dict["player"]:
               
                for gt in data_dict['filter']['GameType']:
                    
                    db_data  = DatabaseApi.getBoxScoreStatsByDateRange('*','BoxScores',['Player','BoxScore_Type'],[player_key,gt],sd,ed,'DESC' if ed<sd else 'ASC')
                    num = len(db_data[0])-1
                    i=0
                    
                    
                    while i<=num:
                        
                        player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][i]))
                        result[player_key+" VS "+player_data_dict[player_key]["Opponent"]+" on " + player_data_dict[player_key]["Date"][4:6]+"/"+player_data_dict[player_key]["Date"][6:8]+"/"+player_data_dict[player_key]["Date"][0:4]] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
                        i=i+1
                    if num >=0:
                        Parser.parse_output(result,player_key,gt,dr[0]+"->"+dr[1])
                        result={}
                    




                    
                    
                

    

    for schedule_key in data_dict["schedule"]:
        pass 

   #print(player_data_dict)
    
    

    return

#main("--player Joel Embiid, Luka Dončić, Giannis Antetokounmpo, Kevin Durant, Domantas Sabonis, Devin Booker, Jayson Tatum, Donovan Mitchell, LaMelo Ball, De'Aaron Fox, Damian Lillard --stats PTS,TRB,AST,boxscores_id,Token,Date --filter L5")
#main("--player Nikola Jokić,Julius Randle, Jalen Brunson,Shai Gilgeous-Alexander,Anthony Davis, Kawhi Leonard,LeBron James --stats PTS,TRB,AST,boxscores_id,Token,Date --filter L10,G")
#main("--player Devin Booker --stats 3P,3PA,boxscores_id,Token,Date --filter L6,H1, 01/10/2024->01/16/2024")
main("--player Zach Collins --stats PTS,Date --filter G,L5, 01/10/2024->01/19/2024")