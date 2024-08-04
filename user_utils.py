import string
import random
from user import User
from connect_mysql import connect_database
from mysql.connector import Error


def generate_library_id():
    #generate random library id and return it
    id = ''.join(random.choices(string.digits, k=10))
    return id

def add_user(user_dict):
    #establish connection
    conn = connect_database()

    #ensure connection and add author to the db first
    if conn is not None:
        try:
            cursor = conn.cursor()
            #get user details from operator
            name = input("Please enter the name of the user you'd like to add: ").strip()
            
            #generate new user's library id
            id = generate_library_id()
            
            #check if generated id is already in use and regenerate if is
            library_id_set = set()
            for user_id in user_dict.keys():
                library_id_set.add(user_dict[user_id].get_library_id())
            while True:
                if id in library_id_set:
                    id = generate_library_id()
                else: #id not already in use
                    break #end loop
            
            #query to insert new user into users table
            query = '''INSERT INTO users (name, library_id)
            VALUES (%s, %s)'''

            #execut query
            cursor.execute(query, (name, id))
            conn.commit()

            #add user to dictionary
            temp_user = User(name, id)
            user_dict[get_user_id_from_library_id(id)] = temp_user

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

def view_user_details(user_dict, book_dict):
    #check for users in dictionary
    if user_dict:
        while True:
            #get info to search from
            query = input("Please input the name or Library ID of the user you'd like to view: ").strip()
            #check for name or id and print info of resulting user
            if not query.isnumeric():
                query = get_user_id_from_name(user_dict, query)
                display_user(user_dict, book_dict, query)
                break
            elif query.isnumeric():
                display_user(user_dict, book_dict, query)
                break
            else:
                print("invalid input, please try again")
    else:
        print("There are currently no users registered at the library")

def display_user(user_dict, book_dict, id):
    #check that id is in dictionary
    if id in user_dict.keys():
        #print resulting information
        print(f"\nName: {user_dict[id].get_name()}")
        print(f"Library ID: {user_dict[id].get_library_id()}")
        print("Currently borrowed books:") 
        temp = user_dict[id].get_borrowed()
        if temp:
            for book in temp:
                print(f'"{book_dict[book].get_title()}" by {book_dict[book].get_author()}')
        else:
            print("This user currently does not have any books borrowed.")
        print("\n") 
    #no users in dictionary
    else:
        print("The user id you provided is not in use by any users")

def display_all_users(user_dict, book_dict):
    #check that there are users in dictionary
    if user_dict:
        #iterate and display users' information
        for id, user in user_dict.items():
            print(f"\nName: {user_dict[id].get_name()}")
            print(f"Library ID: {user_dict[id].get_library_id()}") 
            print("Currently borrowed books:") 
            temp = user_dict[id].get_borrowed()
            if temp:
                for book in temp:
                    print(f'"{book_dict[book].get_title()}" by {book_dict[book].get_author()}')
            else: 
                print("This user currently does not have any books borrowed.")
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

            #SQL Query to get ids from users with name that matches input
            query = "SELECT id FROM users WHERE name LIKE %s"

            #Execute query and store results
            cursor.execute(query, (name,))
            results = cursor.fetchall()

            #check that results came back and how many results come back and choose exact member
            if results:
                #one result
                if len(results) == 1:
                    return_value = results[0][0]
                
                #multiple results and choosing specific user
                elif len(results) > 1:
                    #iterate through results and print for choosing
                    counter = 1
                    for user in results:
                        print(f"{counter}: Name: {user_dict[user[0]].get_name()}") #print user name
                        print(f"   Library ID: {user_dict[user[0]].get_library_id()}") #print the library id
                        counter += 1
                    #choose distinct result to return
                    while True:
                        choice = input("Please input the number of the user you were looking for: ").strip()
                        if int(choice) > 0 and int(choice) <= len(results):
                            return_value = results[int(choice) - 1][0]
                        else:
                            print("Invalid choice. Please Try again")
            
            #no resulsts return none
            else:
                return_value = None
                print("That name does not have a Library ID")

        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("\033[7mError: Value for name is too long.\033[0m")
            else:
                print(f"\033[7mError: {e}\033[0m")
        except KeyError:
            print("\033[7mInvalid choice get_user_id_from_name. Please try again with only numbers\033[0m")

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

            #SQL Query to get the id from the user with the matching library id
            query = "SELECT id FROM users WHERE library_id = %s"

            #Execute query and store results
            cursor.execute(query, (library_id,))
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
        
def load_users_from_db(user_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to get all from users
            query = "SELECT * FROM users"

            #Execute query and store results
            cursor.execute(query)
            results = cursor.fetchall()

            #check that results came back and load into dictionary
            if results:
                for result in results:
                    id, name, library_id = result
                    user_dict[id] = User(name, library_id)
            else:
                raise Error("There are currently no Users in the database")

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