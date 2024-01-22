import DatabaseApi
import Parser




def main(input):

    player_data_dict={}
    result={}
    data_dict = Parser.parse_input(input)
    #print(data_dict)
    
    
    def filter_dates(db_data):
        
        for date_key in data_dict["date"]:
            if '->' in date_key:
                print(db_data)

        



    for player_key in data_dict['player']:

        teams = DatabaseApi.getList('Tm','Players')[0]
        mod_teams=[]
        for team in teams:
            mod_teams.append(team[0])
        
        if player_key in mod_teams:
            data_dict['player'].remove(player_key)
            players= DatabaseApi.getStats('Player','Players','Tm',player_key)[0]
            for p in players:
                data_dict["player"].append(p[0])
    
    if data_dict["filter"]==[]:

        for player_key in data_dict['player']:

            db_data = DatabaseApi.getStats('*','Players','player',player_key)
            player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][0]))
            result[player_key] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
    
    else:
        
        while data_dict["filter"]!=[]:
            
            fil=data_dict["filter"].pop(0)
            
            if (fil[0]=='L' or fil[0]=='F') and fil[1].isnumeric():
                for player_key in data_dict["player"]:
                    
                    db_data  = DatabaseApi.getBoxScoreStats('*','BoxScores',['Player','BoxScore_Type'], [player_key,'G'],'DESC' if fil[0]=='L' else 'ASC') 
                    #filter_dates(db_data)
                    num = int(fil[1:])-1
                    if num >len(db_data[0])-1:
                        num = len(db_data[0])-1
                    i=0
                    
                    
                    while i<=num:
                        
                        player_data_dict[player_key] = dict(zip(db_data[1],db_data[0][i]))
                        result[player_key+" L"+str(i+1)] = { key: player_data_dict[player_key][key] for key in data_dict['stats'] if key in player_data_dict[player_key]}
                        i=i+1
                    Parser.parse_output(result)
                    result={}
            

    

    for schedule_key in data_dict["schedule"]:
        pass 

   #print(player_data_dict)
    
    

    return

#main("--player Joel Embiid, Luka Dončić, Giannis Antetokounmpo, Kevin Durant, Domantas Sabonis, Devin Booker, Jayson Tatum, Donovan Mitchell, LaMelo Ball, De'Aaron Fox, Damian Lillard --stats PTS,AST,TRB,boxscores_id,Token,Date --filter L5")

main("--player DAL --stats PTS,AST,TRB,boxscores_id,Token,Date --filter L5")