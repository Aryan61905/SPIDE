import mysql.connector
from mysql.connector import errorcode
import RosterUpdateAPI


connection = mysql.connector.connect(
                host='127.0.0.1',  # Replace with your MySQL host address
                user='root',    # Replace with your MySQL username
                password='SPIDE2023' # Replace with your MySQL password
            )

cursor = connection.cursor()

database_name = 'SPIDE_LOCAL_DB'  # Replace with your desired database name


cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")


cursor.execute(f"USE {database_name}")
create_table_query = """
        CREATE TABLE IF NOT EXISTS NBA (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_name VARCHAR(255) NOT NULL,
            team_id INT NOT NULL
        )
    """

cursor.execute(create_table_query)
TeamMap={}
TeamMap = RosterUpdateAPI.RosterUpdate()

cursor.close()
connection.close()

