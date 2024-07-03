from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt
import copy

def parse_input(input):
    input_list = input.split('--')
    input_dict = {'player': [], 'team': [], 'stats': [], 'schedule':[],
                  
                  'filter':{ 
                      'GameType':[],
                      'XGames':[],
                      'DateRange':[],
                      'Date':[],
                      'Player':[],
                      'Team':[]
                  }, 
                  
                  }

    for item in input_list:
        if 'player' in item:
            players = item.split('player')[1].strip()
            if players:
                input_dict['player'].extend([p.strip() for p in players.split(',')])

        elif 'team' in item:
            teams = item.split('team')[1].strip()
            if teams:
                input_dict['team'].extend([t.strip() for t in teams.split(',')])
        
        elif 'stats' in item:
            stats = item.split('stats')[1].strip()
            if stats:
                input_dict['stats'].extend([s.strip() for s in stats.split(',')])
        
        elif 'filter' in item:
            #filter : LN, FN, home, away
            filter = item.split('filter')[1].strip()

            if filter:
                
                filter = [f.strip() for f in filter.split(',')]
                
                for i in filter:
                    
                    if i in ['Q1','Q2','Q3','Q4','H1','H2','G','OT1','OT2']:
                        input_dict["filter"]['GameType'].append(i)

                    elif i[0] in 'LF' and i[1:].isdigit():
                        input_dict["filter"]['XGames'].append(i)
                    
                    elif '->' in i:
                        input_dict["filter"]['DateRange'].append(i)
                    
                    elif i[0:2].isdigit() and i[2] == '/' and i[3:5].isdigit() and i[5] == '/' and i[6:8].isdigit():
                        input_dict["filter"]['Date'].append(i)
                    
                    elif i[0] in '+-':
                        input_dict["filter"]["Player"].append(i)
        
        elif 'schedule' in item:
            schedule = item.split('schedule')[1].strip()
            if schedule:
                input_dict['schedule'].extend([s.strip() for s in schedule.split(',')])

    return input_dict



def parse_output(output,player,GameType,XGames,filterPlayer=""):
    print(filterPlayer)
    rows = list(output.keys())
    columns = list(output[rows[0]].keys())
    table_data = []
    for r in rows:
        row = [r]+[output[r][c] for c in columns]
        table_data.append(row)
    headers = [player+" "+ XGames+ " in "+ GameType+ " "+ filterPlayer]+ columns
    table  = tabulate(table_data,headers=headers,tablefmt='pretty')
    print(table)
    return {player:[headers]+table_data}
    
    

def parse_output_special(output,player,GameType,XGames):
    #print(output)
    print(output)
    my_copy = copy.deepcopy(output)
    return ({player:my_copy})
    
    
    
    

    

    
