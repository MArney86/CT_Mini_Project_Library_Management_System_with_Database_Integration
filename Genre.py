from connect_mysql import connect_database
from mysql.connector import Error
from genre_utils import get_genre_id_from_db
class Genre:
    def __init__(self, name, description, category):
        self._genre_id = get_genre_id_from_db(name, category)
        self._name = name
        self._description = description
        self._category = category

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
                UPDATE Genres
                SET name = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (name, self._genre_id))
                conn.commit()
                self._name = name
                print("Genre name updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Unable to update genre name\nError: Value for name is too long.")
            
                else:
                    print(f"Unable to update title\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()


    def get_description(self):
        return self._description
    
    def set_description(self, description):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Genres
                SET name = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (description, self._genre_id))
                conn.commit()
                self._description = description
                print("Genre name updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Unable to update genre description\nError: Value for name is too long.")
            
                else:
                    print(f"Unable to update description\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_category(self):
        return self._category
    
    def set_category(self, category):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Genres
                SET category = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (category, self._genre_id))
                conn.commit()
                self._category = category
                print("Genre name updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Unable to update genre name\nError: Value for name is too long.")
            
                else:
                    print(f"Unable to update title\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
