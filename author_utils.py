from author import Author
from mysql.connector import Error
from connect_mysql import connect_database

def add_author(author_dict):
    #get author details from operator
    name = input("Please enter the name of the Author you wish to add: ").strip()
    bio = input("Please enter a biography for the Author you wish to add: ").strip()
    
    #establish connection
    conn = connect_database()

    #ensure connection and add author to the db first
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "INSERT INTO authors (name, biography) VALUES (%s, %s)" #inserts new member in the Members table using the information passed to the function

            #Execute query and add author to author dictionary
            cursor.execute(query, (name, bio))
            conn.commit()
            #add author to author dictionary
            author_temp = Author(name, bio)
            author_dict[author_temp.get_author_id()] =  author_temp
            print("Author added successfully")
        
        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("Error: Value for name is too long.")
            else:
                print(f"Error: {e}") #general error

def view_author_details(author_dict, book_dict):
    while True:
        name = input("Please enter that name of the author you'd like to view: ").strip() #get name of author from operator
        author_id = get_author(author_dict, book_dict, name)
        if author_id in author_dict.keys(): #check name is in keys of dictionary
            display_author(author_dict, author_id) #display the author's information
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
        for author_id in author_dict.keys(): #iterate through authors in dictionary
            display_author(author_dict, author_id) #print details of author to user
    else:
        print("There are currently no authors in the library records")

def get_author(author_dict, book_dict, name):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT id FROM authors WHERE name LIKE %s" #inserts new member in the Members table using the information passed to the function

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
                            print(f"{counter}. {author_dict[result[0]].get_name()}:  {author_dict[result[0]].get_biography()}")
                            counter += 1
                    while True: #loop in case of invalid inputs
                        choice = input('Please input the number of the specific Author you were looking for')
                        
                        #verify valid choice and set to return selected author
                        if int(choice) > 0 and int(choice) <= len(results):
                            return_value = results[int(choice) - 1][0]
                        else: #invalid choice
                            print("That was not a valid choice. Please try again")
            else:
                return_value = None
                raise Error("The Author was not found")

        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("Error: Value for name is too long.")
            else:
                print(f"Error: {e}") #general error
        except ValueError:
            print("That was not a valid choice. Please try again using only numbers")

        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
            return return_value

def load_authors_from_db(author_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT * FROM authors" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query)

            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and how many results come back
            if results:
                for result in results:
                    id, name, biography = result
                    author_dict[id] = Author(name, biography)
            else:
                raise Error("There are currently no Authors in the database")

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