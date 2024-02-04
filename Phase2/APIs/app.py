from flask import Flask, jsonify,render_template
import requests
from conncect_db import connect_to_database, close_database_connection
from main import main
import pandas as pd

app = Flask(__name__)



@app.route('/input/<msg>')
def process_input(msg):

    input_data = msg
    conn,cursor= connect_to_database('Main')
    output = main(msg,conn,cursor)
    close_database_connection(conn)
    
    df1 = pd.DataFrame(output[0][0])
    df1.columns = df1.iloc[0]
    df1 = df1[1:]
   
    df2 = pd.DataFrame(output[0][2])
    df2.columns = df2.iloc[0]
    df2 = df1[2:]
    print(df2)
    

    
    return (output[0][0]+output[0][2])

@app.route('/')
def Home():
    data = "WELCOME"
    return jsonify(data)
    

if __name__ == '__main__':
    app.run(debug=True)
