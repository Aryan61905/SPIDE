import mysql.connector

def ConnectDB():
    connection = mysql.connector.connect(
                    host='127.0.0.1',  # Replace with your MySQL host address
                    user='root',    # Replace with your MySQL username
                    password='SPIDE2023' # Replace with your MySQL password
                )

    cursor = connection.cursor()

    database_name = 'SPIDE_LOCAL_DB'  # Replace with your desired database name


    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")


    cursor.execute(f"USE {database_name}")
    return [cursor,connection]

def DisconnectDB(cursor,connection):
    connection.commit()
    cursor.close()
    connection.close()
