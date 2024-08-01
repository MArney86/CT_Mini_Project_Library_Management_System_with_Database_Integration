import Author
from mysql.connector import Error
from connect_mysql import connect_database
from book_utils import get_books_by_author
def add_author(author_dict):
    name = input("Please enter the name of the Author you wish to add: ").strip() #get name from user
    bio = input("Please enter a biography for the Author you wish to add: ").strip() #get biography from user
    
    #establish connection
    conn = connect_database()

    #ensure connection and add author to the db first
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "INSERT INTO Authors (name, bio) VALUES (%s, %s)" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (name, bio))
            conn.commit()
            print("Author added successfully")
        
        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("Error: Value for name is too long.")
            else:
                print(f"Error: {e}") #general error

    #add author to author dictionary
    author_temp = Author(name, bio)
    author_dict[author_temp.get_author_id()] =  author_temp

def view_author_details(author_dict):
    while True:
        name = input("Please enter that name of the author you'd like to view: ").strip() #get name of author from operator
        if name.lower() in author_dict.keys(): #check name is in keys of dictionary
            display_author(author_dict, name) #display the author's information
            break #end loop
        else: #author doesn't exist in keys
            print("That Author's name is not in the library's list of authors.") #notify user that author is not in library
            choice = input("Would you like to add the Author? (yes/no): ").strip() #offer to add
            if choice == 'yes': #operator chooses to add
                add_author(author_dict) #add author
            else:
                break

def display_author(author_dict, author_id):
    print(f"\nName: {author_dict[author_id].get_name()}") #print author name to operator
    print(f"Biography: {author_dict[author_id].get_biography()}") #print author's biography to operator

def display_all_authors(author_dict):
    if author_dict: #check that there are authors in the dictionary
        for name in author_dict.keys(): #iterate through authors in dictionary
            display_author(author_dict, name) #print details of author to user
    else:
        print("There are currently no authors in the library records")

def get_author_id_from_db(name, bio):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Authors id WHERE name = %s AND bio = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (name, bio))
            
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

def get_author(author_dict, name):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Authors id WHERE name = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (name,))
            
            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and how many results come back
            if results:
                
                #one result
                if len(results) == 1:
                    return_value = results[0][0]
                
                #multiple results
                else:
                    print("Authors with the name you chose:")
                    
                    counter = 1
                    for result in results:
                        if get_books_by_author()[0][0]:
                            print(f"{counter}. {author_dict[result[0]].get_name()} author of {get_books_by_author()[0][0]}")
                        else:
                            print(f"{counter}. {author_dict[result[0]].get_name()}")
                    while True: #loop in case of invalid inputs
                        choice = input('Please input the number of the Author you were looking for')
                        
                        #verify valid choice and set to return selected author
                        if int(choice) > 0 and int(choice) <= len(results):
                            return_value = result[choice - 1][0]
                        else: #invalid choice
                            print("That was not a valid choice. Please try again")
            else:
                raise Error("The Author was not found")

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
