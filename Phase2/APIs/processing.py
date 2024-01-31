

def getTeams():
        teams = DatabaseApi.getList('Tm','Players')[0]
        mod_teams=[]
        for team in teams:
            mod_teams.append(team[0])
        return mod_teams
    
def populatePlayers():
    for player_key in data_dict['player']:
        
        teams = getTeams()
        
        if player_key in teams:
            
            players= DatabaseApi.getStats('Player','Players','Tm',player_key)[0]
            for p in players:
                data_dict["player"].append(p[-1])
    
    data_dict['player'] = [val for val in data_dict['player'] if val not in teams]

def getXGames(x):
    
    result={}
    player_data_dict={}
    for player_key in data_dict["player"]:
        
        for gt in data_dict['filter']['GameType']:
            special = {'AVG':{},'SUM':{}}
            
            for i in data_dict['stats']:
                if '(' in i and i[:i.index('(')] in special.keys():
                    special[i[:i.index('(')]][i[i.index('(')+1:i.index(')')]]=0
                    data_dict['stats'][data_dict['stats'].index(i)]= i[i.index('(')+1:i.index(')')]
                
            select_v = ', '.join(['\"{}\"'.format(item) if item[0].isdigit() else '{}'.format(item) for item in data_dict['stats']])
            select_v += ', Opponent'
            num = int(x[1:])-1
            db_data  = DatabaseApi.getBoxScoreStats(select_v,'BoxScores',['Player','BoxScore_Type'], [player_key,gt],num,'DESC' if x[0]=='L' else 'ASC') 
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
            
            return special




