import mysql.connector
from mysql.connector import Error

def connect_database():
    #login details
    db_name = 'library_management_system_db'
    user = 'root'
    password = 'your password here'
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

        return conn
    
    #Error during connection
    except Error as e:
        print(f"Error: {e}")
        return None

def establish_db():
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()
            #query to check status of tables in database
            query = "SHOW TABLES"
            cursor.execute(query)
            tables = cursor.fetchall()
            table_set = set()
            if tables:
                for table in tables:
                    table_set.add(table[0])
                necessary_tables = {'authors', 'genres', 'users', 'books', 'borrowed_books'}
                needed_tables = necessary_tables.difference(table_set)
                if not needed_tables:
                    print("All tables are setup")
                else:
                    print("Setting up missing tables")
                    if 'genres' in needed_tables:
                        setup_tables('genres')
                           
                    if 'authors' in needed_tables:
                        setup_tables('authors')

                    if 'users' in needed_tables:
                        setup_tables('users')

                    if 'books' in needed_tables:
                        setup_tables('books')

                    if 'borrowed_books' in needed_tables:
                        setup_tables('borrowed_books')

            else:
                print("Tables not setup, creating tables")
                setup_tables('genres')
                setup_tables('authors')
                setup_tables('users')
                setup_tables('books')
                setup_tables('borrowed_books')

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

def setup_tables(table):
    #establish connection
    conn = connect_database()

    #ensure connection and update name in db
    if conn is not None:
        try:
            cursor = conn.cursor()

            genres_query = '''
            CREATE TABLE genres (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            category VARCHAR(50)
            )'''

            authors_query = '''
            CREATE TABLE authors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            biography TEXT
            )'''

            users_query = '''
            CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            library_id VARCHAR(10) NOT NULL UNIQUE
            )'''

            books_query = '''
            CREATE TABLE books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INT,
            genre_id INT,
            isbn VARCHAR(13) NOT NULL,
            publication_date DATE,
            availability BOOLEAN DEFAULT 1,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (genre_id) REFERENCES genres(id)
            )'''

            borrow_books_query = '''
            CREATE TABLE borrowed_books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            book_id INT,
            borrow_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
            )'''

            if table == 'genres':
                cursor.execute(genres_query)
                conn.commit()
                print("Tables: genres created")

            elif table == 'authors':
                cursor.execute(authors_query)
                conn.commit()
                print("Tables: authors created")

            elif table == 'users':
                cursor.execute(users_query)
                conn.commit()
                print("Tables: users created")

            elif table == 'books':
                cursor.execute(books_query)
                conn.commit()
                print("Tables: books created")

            elif table == 'borrowed_books':
                cursor.execute(borrow_books_query)
                conn.commit()
                print("Tables: borrowed_books created")

            else:
                raise Error("Invalid arguement for setup_tables function")

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