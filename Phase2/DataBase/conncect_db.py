import sqlite3



def connect_to_database():
    conn = sqlite3.connect('NBA_Player_Database.db')
    cursor = conn.cursor()
    return conn, cursor

# Close the database connection
def close_database_connection(conn):
    conn.commit()
    conn.close()