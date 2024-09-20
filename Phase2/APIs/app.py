from flask import Flask, jsonify, request
from flask_cors import CORS
from conncect_db import connect_to_database, close_database_connection
from main import main
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/terminal', methods=['POST'])
def handle_command():
    data = request.get_json()
    command = data.get('command')
    
    # Process the command
    if command is None:
        return jsonify({'error': 'No command provided'}), 400
    
    response = process_command(command)
    
    res = response[0]
    data={}
    #print(res)
    for r in res:
        for k in r.keys():
            if k in data:
                data[k].append(r[k])
            else:
                data[k] = r[k]

    return jsonify(data)

@app.route('/api/prompt',methods=['POST'])
def prompt():
    
    data = request.get_json()
    
    prompt_input = data.get('searchTerm')
    print(prompt_input)
    output = process_prompt(prompt_input)
    return jsonify(output)

def process_prompt(prompt_input):
    conn,cursor = connect_to_database('Main')
    def levenshtein(a, b):
        if a == b:
            return 0
        if len(a) == 0:
            return len(b)
        if len(b) == 0:
            return len(a)
        
        v0 = list(range(len(b) + 1))
        v1 = [0] * (len(b) + 1)
        
        for i in range(len(a)):
            v1[0] = i + 1
            for j in range(len(b)):
                cost = 0 if a[i] == b[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            v0 = v1[:]
        
        return v1[len(b)]
    conn.create_function("LEVENSHTEIN", 2, levenshtein)
    query = """
        SELECT player
        FROM players
        ORDER BY LEVENSHTEIN(player, ?) ASC
        LIMIT 5;
    """
    
    cursor.execute(query,(prompt_input,))
    output = cursor.fetchall()
    
    close_database_connection(conn)
    return output

def process_command(command):
    # You can implement your command processing logic here
    conn,cursor= connect_to_database('Main')
    output = main(command,conn,cursor)
    close_database_connection(conn)
    return output

if __name__ == '__main__':
    app.run(debug=True,port=8000)
    #process_command("--player Giannis Antetokounmpo --stats AVG(PTS),AVG(TRB),AVG(AST),AVG(PTS+TRB+AST),Team --filter G,L5, -Damian Lilard")

