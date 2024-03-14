from flask import Flask, jsonify, request
from flask_cors import CORS
from conncect_db import connect_to_database, close_database_connection
from main import main
import pandas as pd

app = Flask(__name__)


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
    for r in res:
        for k in r.keys():
            if k in data:
                data[k].append(r[k])
            else:
                data[k] = r[k]

    return jsonify(data)



def process_command(command):
    # You can implement your command processing logic here
    conn,cursor= connect_to_database('Main')
    output = main(command,conn,cursor)
    close_database_connection(conn)
    return output

if __name__ == '__main__':
    app.run(debug=True,port=8000)
    #process_command("--player Deandre Ayton, Richaun Holmes, Immanuel Quickley, Vasilije Micić, Gary Trent Jr., Charles Bassey, Josh Hart, Chris Boucher, Marcus Smart, Kelly Olynyk, Dalano Banton, Dejounte Murray, Brice Sensabaugh, James Wiseman, Jontay Porter, Jaylen Brown, Collin Gillespie, Damian Jones, Naz Reid, Nate Hinton, John Konchar, Simone Fontecchio, P.J. Tucker, Jock Landale, Paul Reed, Nickeil Alexander-Walker, Luke Kornet, Jalen McDaniels, Kevin Durant, GG Jackson II, Trayce Jackson-Davis, Luka Garza, Cam Thomas, Julian Champagnie, Kyle Kuzma, Gradey Dick, Corey Kispert, Grant Williams, Trey Jemison, Kelly Oubre Jr. --stats AVG(PTS),AVG(TRB),AVG(AST),AVG(PTS+TRB+AST),Team --filter G, L5")

