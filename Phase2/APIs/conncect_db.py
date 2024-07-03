import sqlite3


db_ids= {
    'Main':'/home/aryan61905/Desktop/SPIDE-develop/Phase2/DataBase/NBA_Player_Database.db',
    'BoxScores': '/Users/roy/Desktop/SPIDE/Phase2/DataBase/BoxScores_Database.db'
    }
def connect_to_database(db_id):
    conn = sqlite3.connect(db_ids[db_id])
    cursor = conn.cursor()
    return conn, cursor

# Close the database connection
def close_database_connection(conn):
    conn.commit()
    conn.close()