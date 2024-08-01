from connect_mysql import connect_database
from mysql.connector import Error
from author_utils import get_author_id_from_db

class Author:
    def __init__(self, name, bio):
        self._author_id = get_author_id_from_db(name, bio)
        self._name = name
        self._biography = bio

    def get_name(self):
        return self._name
    
    def set_name(self, name):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Authors
                SET name = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (name, self._author_id))
                conn.commit()
                self._name = name
                print("Author name updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Error: Value for name is too long.")
            
                else:
                    print(f"Error: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_biography(self):
        return self._biography
    
    def set_biography(self, bio):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Authors
                SET biography = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (bio, self._author_id))
                conn.commit()
                self._biography = bio
                print("Author biography updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Error: Value for name is too long.")
            
                else:
                    print(f"Error: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_author_id(self):
        return self._author_id
