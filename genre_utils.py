from genre import Genre
from connect_mysql import connect_database
from mysql.connector import Error

def add_genre(genre_dict):
    #establish connection
    conn = connect_database()

    #ensure connection and add author to the db first
    if conn is not None:
        try:
            #get genre details from operator
            name = input("Please enter the Genre name : ").strip()
            description = input("Please enter a description for the Genre: ").strip()
            category = input("Please enter the category (Fiction, Non-fiction, Reference, Periodicals) of the Genre: ").strip()

            #establish cursor
            cursor = conn.cursor()

            #SQL Query to insert new genre into table
            query = "INSERT INTO genres (name, description, category) VALUES (%s, %s, %s)"

            #Execute query and add author to author dictionary
            cursor.execute(query, (name, description, category))
            conn.commit()

            #add author to author dictionary
            genre_temp = Genre(name, description, category)
            genre_dict[genre_temp.get_genre_id()] =  genre_temp
            print("Author added successfully")
        
        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("\033[7mError: Value for name is too long.\033[0m")
            else:
                print(f"\033[7mError: {e}\033[0m") 

def view_genre_details(genres_dict):
    while True:
        #get genre name from operator and find it's id
        name = input("Please input the name of the genre you'd like to view the details of: ").strip()
        genre_id = get_genre_id(name)
        
        #chek for genre in dictionay and display information
        if genre_id in genres_dict.keys():
            display_genre(genres_dict, name)
            break
        #genre not found and ask to add
        else:
            print("That genre is not in the library's list of genres.")
            choice = input("Would you like to add the genre? (yes/no): ").strip()
            if choice == 'yes':
                add_genre(genres_dict)

def display_genre(genres_dict, name):
    #verify that genre with name input exists
    if get_genre_id(name):
        #display genre information
        print(f"\nName: {genres_dict[get_genre_id(name)].get_name()}")
        print(f"Description: {genres_dict[get_genre_id(name)].get_description()}") 
        print(f"Category: {genres_dict[get_genre_id(name)].get_category()}") 
    

def display_all_genres(genres_dict):
    #verify that there are genres in the dictionary
    if genres_dict:
        #iterate through genre dictionary and display genre data
        for id in genres_dict.keys(): 
            print(f"\nName: {genres_dict[id].get_name()}")
            print(f"Description: {genres_dict[id].get_description()}")
            print(f"Category: {genres_dict[id].get_category()}")
    else:
        print("There are no genres currently in the library records.")

def get_genre_id(name):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to get genre id using input name
            query = "SELECT id FROM Genres WHERE name = %s" 

            #Execute query
            cursor.execute(query, (name,))
            
            #store result for manipulation
            result = cursor.fetchone()

            #check that results come back and how many results come back and format data for return
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

def get_books_from_genre(name):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to get ids from all books within the input genre
            query = "SELECT id FROM books id WHERE genre_id = %s"

            #Execute query
            cursor.execute(query, (get_genre_id(name),))
            
            #store result for manipulation
            results = cursor.fetchall()
            return_value = []

            #check that results come back and how many results come back then prepare data for return
            if results:
                #one result
                if len(results) == 1:
                    return_value.append(results[0][0])
                #multiple results
                else:
                    for result in results:
                        return_value.append(result[0])
            else:
                return_value = None

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
            return return_value
        
def load_genres_from_db(genre_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to return all from genre
            query = "SELECT * FROM genres" 

            #Execute query
            cursor.execute(query)

            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and load them into the dictionary
            if results:
                for result in results:
                    id, name, description, category = result
                    genre_dict[id] = Genre(name, description, category)
            else:
                raise Error("There are currently no Genres in the database")

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