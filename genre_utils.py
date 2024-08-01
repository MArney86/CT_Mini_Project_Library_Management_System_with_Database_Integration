import Genre
from connect_mysql import connect_database
from mysql.connector import Error

def add_genre(genres_dict):
    name = input("Please enter the Genre name : ") #ask user for name of genre
    description = input("Please enter a description for the Genre: ") #ask user for description of genre
    while True: #loop in case of invalid input
        category = input("Please enter the category (Fiction, Non-fiction, Reference, Periodicals) of the Genre: ").strip() #ask user for category (Fiction, Non-fiction, Reference, Periodicals)
        if category == "Fiction" or category == "Non-fiction" or category == "Reference" or category == "Periodicals": #check that a valid category was entered
            genres_dict[name.lower()] = Genre(name, description, category) #add new genre to genre dictionary using the name as a key for quicker searching
            break #end loop
        else: #invalid category
            print("That category is invalid. Please enter a valid category") #notify operator of invalid input
    return name.lower()

def view_genre_details(genres_dict):
    while True:
        name = input("Please input the name of the genre you'd like to view the details of: ").strip() #get genre name from operator
        if name.lower() in genres_dict.keys(): #check name is in dictionary keys
            display_genre(genres_dict, name) #display genre details
            break #end loop and function
        else: #genre doesn't exist in keys
            print("That genre is not in the library's list of genres.") #notify user that genre is not in library
            choice = input("Would you like to add the genre? (yes/no): ").strip() #offer to add
            if choice == 'yes': #operator chooses to add
                add_genre(genres_dict) #add genre

def display_genre(genres_dict, name):
    if get_genre_id():
        print(f"\nName: {genres_dict[get_genre_id(name)].get_name()}") #print genre name to operator
        print(f"Description: {genres_dict[get_genre_id(name)].get_description()}") #print description to operator 
        print(f"Category: {genres_dict[get_genre_id(name)].get_category()}") #print category to operator
    

def display_all_genres(genres_dict):
    if genres_dict: #verify that there are genres in dictionary
        for name in genres_dict.keys(): #iterate through the genres in the dictionary
            display_genre(genres_dict, name)#print the genre details to user

def get_genre_id(name):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Genres id WHERE name = %s" #inserts new member in the Members table using the information passed to the function

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

def get_genre_id_from_db(name, category):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Books id WHERE name = %s AND library_id = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (name,category))
            
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