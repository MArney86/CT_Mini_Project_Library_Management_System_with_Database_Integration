from book_utils import get_book_id_from_db
import Genre
from connect_mysql import connect_database
from mysql.connector import Error

class Book(Genre):
    def __init__(self, name, descriptor, category, title, author, isbn, pubdate, status = True):
        self._book_id = get_book_id_from_db(title, author, pubdate)
        self._title = title
        self._author_id = author
        self._isbn = isbn
        self._publication_date = pubdate
        self._status = status
        super().__init__(name, descriptor, category)
    
    def get_title(self): #getter for __title
        return self._title #return value of __title

    def set_title(self, title):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Books
                SET title = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (title, self._book_id))
                conn.commit()
                self._title = title
                print("Title updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Unable to update title\nError: Value for title is too long.")
            
                else:
                    print(f"Unable to update title\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_author(self): #getter for __author
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = 'SELECT FROM Authors name WHERE id = %s'

                #Execute query
                cursor.execute(query, (self._author_id,))
                return_value = cursor.fetchone()[0]

            #exceptions
            except Error as e:
                print(f"Unable to get author\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
                    return return_value
    
    def set_author(self, author_id): #setter for __author
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Books
                SET author_id = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (author_id, self._book_id))
                conn.commit()
                self._author = author_id
                print("Author updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Unable to update author\nError: Value for title is too long.")
            
                else:
                    print(f"Unable to update author\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_isbn(self): #getter for __isbn
        return self._isbn #return value of __isbn
    
    def set_isbn(self, isbn): #setter fro __isbn
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Books
                SET isbn = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (isbn, self._book_id))
                conn.commit()
                self._isbn = isbn
                print("ISBN updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Unable to update ISBN\nError: Value for title is too long.")
            
                else:
                    print(f"Unable to update ISBN\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_publication_date(self): #getter for __publication_date
        return self._publication_date #return value of __publication_date
    
    def set_publication_date(self, pubdate): #setter for __publication_date
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Books
                SET title = %s
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (pubdate, self._book_id))
                conn.commit()
                self._publication_date = pubdate
                print("Author name updated successfully")

            #exceptions
            except Error as e:
                if e.errno == 1406:
                    print("Error: Value for title is too long.")
            
                else:
                    print(f"Error: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_status(self): #return value of __status as either 'Available' or 'Borrowed'
        if self._status: #check if __status is True (available)
            return "Available"  #return "Available"
        else: #__status is False
            return "Borrowed" #return "Borrowed"
    
    def set_status_borrowed(self): #setter for setting _status to borrowed
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Books
                SET availability = 0
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (self._book_id,))
                conn.commit()
                self._status = False
                print("Author name updated successfully")

            #exceptions
            except Error as e:
                print(f"Unable to update borrowed status\nError: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def set_status_available(self): #setter for setting __status to Available
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the author's name in the db
                query = '''
                UPDATE Books
                SET availablity = 1
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (self._book_id,))
                conn.commit()
                self._status = True
                print("Author name updated successfully")

            #exceptions
            except Error as e:            
                print(f"Error: {e}") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()