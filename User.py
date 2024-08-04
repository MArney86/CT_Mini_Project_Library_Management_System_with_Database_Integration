from connect_mysql import connect_database
from mysql.connector import Error

class User:
    def __init__(self, name, id):
        self._name = name
        self._library_id = id
        self._user_id = self._get_user_id_from_db()

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
                cursor.execute(query, (name, self._user_id))
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

    def get_library_id(self):
        return self._library_id
    
    def set_library_id(self, library_id):
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
                cursor.execute(query, (library_id, self._user_id))
                conn.commit()
                self._library_id = library_id
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

    def get_borrowed(self):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = 'SELECT book_id FROM borrowed_books WHERE user_id = %s'

                #Execute query then prepare it for returning
                cursor.execute(query, (self._user_id,))
                borrowed = cursor.fetchall()
                if borrowed:
                    return_value = []
                    for book in borrowed:
                        return_value.append(book[0])
                else:
                    return_value = None

            #exceptions
            except Error as e:
                print(f"Unable to get borrowed books\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
                return return_value
            
    def _get_user_id_from_db(self):
        #establish connection
        conn = connect_database()

        #ensure connection
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query
                query = "SELECT id FROM Users WHERE name = %s AND library_id = %s" #inserts new member in the Members table using the information passed to the function

                #Execute query
                cursor.execute(query, (self._name, self._library_id))
            
                #store result for manipulation
                result = cursor.fetchone()

                #check that results come back and how many results come back
                if result:
                    result = result[0]
                else:
                    result = None

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
                return result