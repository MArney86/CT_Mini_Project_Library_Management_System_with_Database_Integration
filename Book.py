from connect_mysql import connect_database
from mysql.connector import Error

class Book():
    def __init__(self, title, genre_id, author, isbn, pubdate, availability = True):
        self._genre_id = genre_id
        self._title = title
        self._author_id = author
        self._isbn = isbn
        self._publication_date = pubdate
        self._availability = availability
        self._book_id = self._get_book_id_from_db()

    def get_book_id(self):
        return self._book_id
    
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

                #SQL Query to update the book's nametitle in the db
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
                    print("\033[7mUnable to update title\nError: Value for title is too long.")
            
                else:
                    print(f"\033[7mUnable to update title\nError: {e}\033[0m") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_genre_id(self):
        return self._genre_id

    def get_genre(self):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to get the name of the genre from the db
                query = 'SELECT name FROM genres WHERE id = %s'

                #Execute query
                cursor.execute(query, (self._genre_id,))
                return_value = cursor.fetchone()[0]

            #exceptions
            except Error as e:
                print(f"\033[7mUnable to get Genre name\nError: {e}\033[0m") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()
                    return return_value

    def get_author(self): #getter for __author
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()
                
                #SQL Query to update the author in the book in the db
                query = 'SELECT author_id FROM books WHERE id = %s'

                #Execute query
                cursor.execute(query, (self._book_id,))
                temp = cursor.fetchone()
                if temp:            
                    return_value = temp[0]
                else:
                    return_value = None

            #exceptions
            except Error as e:
                print(f"\033[7mUnable to get author\nError: {e}\033[0m")

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

                #SQL Query to update the book's author in the db
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
                    print("\033[7mUnable to update author\nError: Value for title is too long.\033[0m")
                else:
                    print(f"\033[7mUnable to update author\nError: {e}\033[0m")

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_isbn(self):
        return self._isbn
    
    def set_isbn(self, isbn): #setter fro __isbn
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the book's isbn in the db
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
                    print("\033[7mUnable to update ISBN\nError: Value for title is too long.\033[0m")
                else:
                    print(f"\033[7mUnable to update ISBN\nError: {e}\033[0m")

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_publication_date(self):
        return self._publication_date 
    
    def set_publication_date(self, pubdate):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the book's publication date in the db
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
                    print("\033[7mError: Value for title is too long.\033[0m")
                else:
                    print(f"\033[7mError: {e}\033[0m")

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def get_availability(self):
        #return available or borrowed depending on value in class
        if self._availability:
            return "Available"
        else:
            return "Borrowed"
            
    def set_borrowed(self):
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the book's availability in the db
                query = '''
                UPDATE Books
                SET availability = 0
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (self._book_id,))
                conn.commit()
                self._availability = False
                print(f"{self._title} was set to borrowed")

            #exceptions
            except Error as e:
                print(f"\033[7mUnable to update borrowed status\nError: {e}\033[0m")

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def set_available(self): #setter for setting __status to Available
        #establish connection
        conn = connect_database()

        #ensure connection and update name in db
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to update the book's availability in the db
                query = '''
                UPDATE books
                SET availability = 1
                WHERE id = %s
                '''

                #Execute query
                cursor.execute(query, (self._book_id,))
                conn.commit()
                self._availability = True
                print(f"{self._title} was set to Available")

            #exceptions
            except Error as e:            
                print(f"\033[7mError: {e}\033[0m") #general error

            #close connections
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

    def _get_book_id_from_db(self):
        #establish connection
        conn = connect_database()

        #ensure connection
        if conn is not None:
            try:
                #establish cursor
                cursor = conn.cursor()

                #SQL Query to get id from book with matching isbn
                query = "SELECT id FROM Books WHERE isbn = %s" 

                #Execute query
                cursor.execute(query, (self._isbn,))
            
                #store result for manipulation
                result = cursor.fetchone()

                #check that results come back and package for return
                if result:
                    result = result[0]
                #no results return none
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