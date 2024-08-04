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

            #SQL Query
            query = "INSERT INTO genres (name, description, category) VALUES (%s, %s, %s)" #inserts new member in the Members table using the information passed to the function

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
                print("Error: Value for name is too long.")
            else:
                print(f"Error: {e}") #general error

def view_genre_details(genres_dict):
    while True:
        name = input("Please input the name of the genre you'd like to view the details of: ").strip() #get genre name from operator
        genre_id = get_genre_id(name)
        if genre_id in genres_dict.keys(): #check name is in dictionary keys
            display_genre(genres_dict, name) #display genre details
            break #end loop and function
        else: #genre doesn't exist in keys
            print("That genre is not in the library's list of genres.") #notify user that genre is not in library
            choice = input("Would you like to add the genre? (yes/no): ").strip() #offer to add
            if choice == 'yes': #operator chooses to add
                add_genre(genres_dict) #add genre

def display_genre(genres_dict, name):
    if get_genre_id(name):
        print(f"\nName: {genres_dict[get_genre_id(name)].get_name()}") #print genre name to operator
        print(f"Description: {genres_dict[get_genre_id(name)].get_description()}") #print description to operator 
        print(f"Category: {genres_dict[get_genre_id(name)].get_category()}") #print category to operator
    

def display_all_genres(genres_dict):
    if genres_dict: #verify that there are genres in dictionary
        for id in genres_dict.keys(): #iterate through the genres in the dictionary
            print(f"\nName: {genres_dict[id].get_name()}") #print genre name to operator
            print(f"Description: {genres_dict[id].get_description()}") #print description to operator 
            print(f"Category: {genres_dict[id].get_category()}") #print category to operator
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

            #SQL Query
            query = "SELECT id FROM Genres WHERE name = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (name,))
            
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

def get_books_from_genre(name):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT id FROM books id WHERE genre_id = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (get_genre_id(name),))
            
            #store result for manipulation
            results = cursor.fetchall()
            return_value = []

            #check that results come back and how many results come back
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
                print("Error: Value for name is too long.")
            
            else:
                print(f"Error: {e}") #general error

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

            #SQL Query
            query = "SELECT * FROM genres" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query)

            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and how many results come back
            if results:
                for result in results:
                    id, name, description, category = result
                    genre_dict[id] = Genre(name, description, category)
            else:
                raise Error("There are currently no Genres in the database")

        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("Error: Value for name is too long.")
            else:
                print(f"Error: {e}")

        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()