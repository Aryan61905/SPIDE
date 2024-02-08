from flask import Flask, jsonify, request
from flask_cors import CORS
from conncect_db import connect_to_database, close_database_connection
from main import main
import pandas as pd

app = Flask(__name__)


app = Flask(__name__)
CORS(app)
#--player Paul George,Jayson Tatum--stats PTS,TRB,AST, AVG(PTS+TRB+AST),Date,MP --filter L5,G
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
    
    for r in range(len(res)):
        
        if type(res[r][0])==dict:
            data[str(res[r][1])].append(res[r][0])
        elif type(res[r][0])==list:
            data[str(res[r][0][0].split()[0]+" "+res[r][0][0].split()[1])] = res[r]
    print(data)
    return jsonify(data)

def process_command(command):
    # You can implement your command processing logic here
    conn,cursor= connect_to_database('Main')
    output = main(command,conn,cursor)
    close_database_connection(conn)
    return output

if __name__ == '__main__':
    app.run(debug=True,port=8000)

