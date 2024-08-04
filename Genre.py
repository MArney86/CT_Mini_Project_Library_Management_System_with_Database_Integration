from connect_mysql import connect_database
from mysql.connector import Error

class Genre:
    def __init__(self, name, description, category):
        self._name = name
        self._description = description
        self._category = category
        self._genre_id = self._get_genre_id_from_db()

    def get_genre_id(self):
        return self._genre_id

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

                #SQL Query to update the genre's name in the db
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
                    print("\033[7mUnable to update genre name\nError: Value for name is too long.\033[0m")
                else:
                    print(f"\033[7mUnable to update title\nError: {e}\033[0m")

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

                #SQL Query to update the genre's description in the db
                query = '''
                UPDATE Genres
                SET name = %s
                WHERE id = %s
                '''

                #Execute query and update object
                cursor.execute(query, (description, self._genre_id))
                conn.commit()
                self._description = description
                print("Genre name updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("\033[7mUnable to update genre description\nError: Value for name is too long.\033[0m")
                else:
                    print(f"\033[7mUnable to update description\nError: {e}\033[0m")

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

                #SQL Query to update the genre's category in the db
                query = '''
                UPDATE Genres
                SET category = %s
                WHERE id = %s
                '''

                #Execute query and update object
                cursor.execute(query, (category, self._genre_id))
                conn.commit()
                self._category = category
                print("Genre name updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("\033[7mUnable to update genre name\nError: Value for name is too long.\033[0m")
                else:
                    print(f"\033[7mUnable to update title\nError: {e}\033[0m")

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def _get_genre_id_from_db(self):
        #establish connection
        conn = connect_database()

        #ensure connection
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to get genre id from the name and description
                query = "SELECT id FROM genres WHERE name = %s AND description = %s"
                #Execute query and store results
                cursor.execute(query, (self._name,self._description))
                result = cursor.fetchone()

                #check that results come back and format for return
                if result:
                    result = result[0]
                else:
                    result = None

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("\033[7mError: Value for name is too long.\033[0m")
                else:
                    print(f"\033[7mError: {e}\033[0m")

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
                return result