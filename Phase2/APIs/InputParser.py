
def parse_input(input_string):
    input_list = input_string.split('--')
    input_dict = {'player': [], 'team': [], 'stats': [], 'date': []}

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
            teams = item.split('stats')[1].strip()
            if teams:
                input_dict['stats'].extend([t.strip() for t in teams.split(',')])
        
        elif 'date' in item:
            teams = item.split('date')[1].strip()
            if teams:
                input_dict['date'].extend([t.strip() for t in teams.split(',')])

    return input_dict

    

    

    
