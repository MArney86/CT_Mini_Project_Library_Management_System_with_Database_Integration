import string
import random
from user import User
from connect_mysql import connect_database
from mysql.connector import Error


def generate_library_id():
    id = ''.join(random.choices(string.digits, k=10))#generate randomized library id
    return id #return new library id

def add_user(user_dict):
    name = input("Please enter the name of the user you'd like to add: ").strip() #get new user's name
    id = generate_library_id() #generate new user's library id

    while True: #loop incase id already exists
        if id in user_dict.keys(): #check if id already in use
            id = generate_library_id
            break
        else: #id not already in use
            break #end loop

    user_dict[id] = User(name, id) #initialize new user to user dictionary with library id as key
    return id

def view_user_details(user_dict, book_dict):
    if user_dict: #check that user dictionary isn't empty
        while True: #loop in case of invalid input
            query = input("Please input the name or Library ID of the user you'd like to view: ").strip() #ask the operator for user name or library id
            if not query.isnumeric(): #check if input is not Library ID
                query = get_user_id_from_name(user_dict, query) #set query to the id associated with the name
                display_user(user_dict, book_dict, query) #print user details to operator
                break #end loop
            elif query.isnumeric(): #is library id
                display_user(user_dict, book_dict, query)#print user information to operator
                break #end loop
            else: #input is neither letters or numbers
                print("invalid input, please try again") #notify user of invalid input 

def display_user(user_dict, book_dict, id): 
    if id in user_dict.keys(): #check for user id in the user dictionary
        print(f"\nName: {user_dict[id].get_name()}") #print user name
        print(f"Library ID: {user_dict[id].get_library_id()}") #print user Library ID
        print("Currently borrowed books:") #header for borrowed books
        temp = user_dict[id].get_borrowed() #store the borrowed books list
        if temp: #check that list is not empty
            for book in temp: #iterate through the list
                print(f'"{book_dict[book].get_title()}" by {book_dict[book].get_author()}') #print the title and author of the book iterated
        else: #list is empty
            print("This user currently does not have any books borrowed.") #print that there are no borrowed books currently
        print("\n") #spacer for formatting
    else: #user id is not in the user dictionary
        print("The user id you provided is not in use by any users") #notify operator of lack of user with that id

        
def display_all_users(user_dict, book_dict):
    if user_dict:
        for id, user in user_dict.items(): #iterate through users in the dictionary
            print(f"\nName: {user_dict[id].get_name()}") #print user name
            print(f"Library ID: {user_dict[id].get_library_id()}") #print user Library ID
            print("Currently borrowed books:") #header for borrowed books
            temp = user_dict[id].get_borrowed() #store the borrowed books list
            if temp: #check that list is not empty
                for book in temp: #iterate through the list
                    print(f'"{book_dict[book].get_title()}" by {book_dict[book].get_author()}') #print the title and author of the book iterated
            else: #list is empty
                print("This user currently does not have any books borrowed.") #print that there are no borrowed books currently
    else:
        print("There are currently no users registered at the library")

def get_user_id_from_name(user_dict, name):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Users id WHERE name = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (name,))
            
            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and how many results come back and choose exact member
            if results:
                #one result
                if len(results) == 1: #check that we found users and that there is only 1
                    return_value = results[0][0] #return value of __library_id from found user
                #multiple results and choosing specific user
                elif len(results) > 1:
                    counter = 1
                    for user in results:
                        print(f"{counter}: Name: {user_dict[user].get_name()}") #print user name
                        print(f"   Library ID: {user_dict[user].get_library_id()}") #print the library id
                        counter += 1
                    while True:
                        choice = int(input("Please input the number of the user you were looking for: ").strip())
                        if choice > 0 and choice <= len(results):
                            return_value = results[choice - 1][0]
                        else:
                            print("Invalid choice. Please Try again")
            #no resulsts
            else:
                print("That name does not have a Library ID") #notify operator that user is not found

        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("Error: Value for name is too long.")
            else:
                print(f"Error: {e}") #general error
        except KeyError:
            print("Invalid choice. Please try again with only numbers")

        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            return return_value

def get_user_id_from_library_id(library_id):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Users id WHERE library_id = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (library_id,))
            
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
        
def load_users_from_db(user_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT * FROM users"

            #Execute query
            cursor.execute(query)

            #store result for manipulation
            results = cursor.fetchall()

            #check that results came back and how many results came back
            if results:
                for result in results:
                    id, name, library_id = result
                    user_dict[id] = User(name, library_id)
            else:
                raise Error("There are currently no Users in the database")

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