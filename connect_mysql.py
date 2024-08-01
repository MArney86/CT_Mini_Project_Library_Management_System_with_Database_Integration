import mysql.connector
from mysql.connector import Error

def connect_database():
    #login details
    db_name = 'fitness_center_db'
    user = 'root'
    password = '6yhn*UHB6tfc'
    host = 'localhost'

    #attempt the connection with error handling
    try:
        #make connection with MySQL
        conn = mysql.connector.connect(
            database=db_name,
            user = user,
            password = password,
            host = host
        )

        print("Connected to MySQL database successfully")
        return conn
    
    #Error during connection
    except Error as e:
        print(f"Error: {e}")
        return None
