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

            #SQL Query to insert new author
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
                print("\033[7mError: Value for name is too long.\033[0m")
            else:
                print(f"\033[7mError: {e}\033[0m")

def view_author_details(author_dict, book_dict):
    #ensure there are authors to display
    if author_dict:
        while True:
            #get info from operator
            name = input("Please enter that name of the author you'd like to view: ").strip()
        
            #get the id of the searched for author 
            author_id = get_author(author_dict, book_dict, name)

            #check that author is in the list of authors and display
            if author_id in author_dict.keys():
                display_author(author_dict, author_id)
                break
            else: #author doesn't exist in keys or is not in db and notify
                print("That Author's name is not in the library's list of authors.")

                #ask user if they want to add author
                choice = input("Would you like to add the Author? (yes/no): ").strip()
                if choice == 'yes':
                    add_author(author_dict)
                else:
                    break
    #notify of lack of authors
    else:
        print("There are currently no authors in the library records")


def display_author(author_dict, author_id):
    #display information about the author with the input id
    print(f"\nName: {author_dict[author_id].get_name()}")
    print(f"Biography: {author_dict[author_id].get_biography()}")

def display_all_authors(author_dict):
    #check that there are authors already
    if author_dict:
        #iterate through authors and display their info
        for author_id in author_dict.keys():
            display_author(author_dict, author_id)
    #display to operator that there are no authors to display
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

            #SQL Query go retrieve the id of the author input
            query = "SELECT id FROM authors WHERE name LIKE %s" #inserts new member in the Members table using the information passed to the function

            #Execute query and store results
            cursor.execute(query, (name,))
            results = cursor.fetchall()

            #check that results came back
            if results:
                #one result and setup for return
                if len(results) == 1:
                    return_value = results[0][0]
                
                #multiple results and choose which one to return
                else:
                    print("Authors with the name you chose:")
                    
                    #display results with number to choose
                    counter = 1
                    for result in results:
                            print(f"{counter}. {author_dict[result[0]].get_name()}:  {author_dict[result[0]].get_biography()}")
                            counter += 1
                    #choose result to return
                    while True:
                        choice = input('Please input the number of the specific Author you were looking for')
                        
                        #verify valid choice and set to return selected author
                        if int(choice) > 0 and int(choice) <= len(results):
                            return_value = results[int(choice) - 1][0]
                        else:
                            print("That was not a valid choice. Please try again")
            else:
                return_value = None

        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("\033[7mError: Value for name is too long.\033[0m")
            else:
                print(f"\033[7mError: {e}\033[0m")
        except ValueError:
            print("\033[7mThat was not a valid choice. Please try again using only numbers\033[0m")

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

            #SQL Query to return all authors
            query = "SELECT * FROM authors"

            #Execute query and store results
            cursor.execute(query)
            results = cursor.fetchall()

            #check that results come back and add them to the author's dictionary
            if results:
                for result in results:
                    id, name, biography = result
                    author_dict[id] = Author(name, biography)
            else:
                print("There are currently no Authors in the database")

        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("\033[7mError: Value for name is too long.\033[0m")
            else:
                print(f"\033[7mError: {e}\033[0m") #general error

        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()