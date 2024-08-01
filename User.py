from user_utils import get_user_id_from_db, get_borrowed_from_db
from connect_mysql import connect_database
from mysql.connector import Error

class User:
    def __init__(self, name, id):
        self._user_id = get_user_id_from_db(name, id)
        self._name = name
        self._library_id = id
        self._borrowed = []

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
        return self._borrowed
    
    def add_borrowed(self, book_dict, book_id):
        formatted = get_borrowed_from_db(self._user_id) + '::' + book_id
                
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Users
                SET borrowed = %s
                WHERE id = %s
                '''

                #Execute query then update User
                cursor.execute(query, (formatted, self._user_id))
                conn.commit()
                self._borrowed.extend(book_id)
                print(f"{self._name}(ID:{self._library_id}) has borrowed {book_dict[book_id].get_title()} by {book_dict[book_id].get_author()}")

            #exceptions
            except Error as e:
                print(f"Unable to update borrowed books\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def remove_borrowed(self, book_dict, book_id):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                if book_id in self.get_borrowed():
                    borrowed_copy = self.get_borrowed()
                    borrowed_copy.remove(book_id)
                    formatted = f'{borrowed_copy[0]}'
                    if len(borrowed_copy) > 1:
                        i = 1
                        for i in range(len(borrowed_copy)):
                            formatted = formatted + '::' + {borrowed_copy[i]}
                    else:
                        raise Error(f"That title was not borrowed by {self._name}")

                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Users
                SET borrowed = %s
                WHERE id = %s
                '''

                #Execute query then update User
                cursor.execute(query, (formatted, self._user_id))
                conn.commit()
                self._borrowed.remove(book_id)
                print(f"{self._name} has returned {book_dict[book_id].get_title()} by {book_dict[book_id].get_author()}")

            #exceptions
            except Error as e:
                print(f"Unable to update borrowed books\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
    
    def set_borrowed(self, borrowed_list):
        formatted = f'{borrowed_list[0]}'
        if len(borrowed_list) > 1:
            i = 1
            for i in range(len(borrowed_list)):
                formatted = formatted + '::' + {borrowed_list[i]}
        
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Users
                SET borrowed = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (formatted, self._user_id))
                conn.commit()
                self._borrowed.extend(borrowed_list)
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