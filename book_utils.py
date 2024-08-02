from book import Book
import genre_utils as gu
import datetime as dt
import user_utils as uu
from author_utils import get_author
from connect_mysql import connect_database
from mysql.connector import Error



def book_id_from_title(book_dict, author_dict, title): #function to return the isbn of a book by its title
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Books id WHERE name = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (title,))
            
            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and how many results come back
            if results:
                
                #one result
                if len(results) == 1:
                    return_value = results[0][0]
                
                #multiple results
                else:
                    print("Books with the title you chose:")
                    
                    counter = 1
                    for result in results:
                        print(f"{counter}. {book_dict[result[0]].get_title()} by  {author_dict[book_dict[result[0]].get_author()].get_name()}")
                        counter += 1
                    #choose author
                    while True:
                        choice = input('Please input the number of the book you were looking for')
                        
                        #verify valid choice and set to return selected author
                        if int(choice) > 0 and int(choice) <= len(results):
                            return_value = result[choice - 1][0]
                        else:
                            print("That was not a valid choice. Please try again")
            else:
                raise Error("That title was not found")
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
    
def is_valid_date(user_date): #function to validate date inputs
    result = True #initialize returned value to true

    try: 
        year_str, month_str, day_str = user_date.split('-') #split input date
        try: 
            dt.date(year = int(year_str), month = int(month_str), day = int(day_str)) #attempt to add values to a date object
        except ValueError: #value error from date() attempt
            result = False #return value of false
    except ValueError: #value error from split attempt
        result = False #return value of false

    return result #no errors, return true value

def add_book(book_dict, genre_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to add the book to the Books table
            query = "INSERT INTO Books (title, genre, author, isbn, publication_date) VALUES (%s, %s, %s, %s, %s)"

            
            title = input("Please enter the title of the book you'd like to add: ").strip() #get title from operator
            author = get_author(input("Please enter the Author of the book you'd like to add: ")).strip() #get author from operator
            isbn = input("Please enter the ISBN for the book you'd like to add: ").strip() #get isbn from operator

            while True: #loop incase of invalid inputs
                pub_date = input("Please enter the publication date of the book you'd like to add (YYYY-MM-DD format): ").strip() #get publication date from operator
                if is_valid_date(pub_date): #check that input is valid
                    db_date = pub_date
                    year_str, month_str, day_str = pub_date.split('-') #split input date
                    pub_date = dt.date(year = int(year_str), month = int(month_str), day = int(day_str)) #add publication date as date object
                    break #end loop
                else: #invalid input
                    print("Invalid date, please try again") #notify operator and continue loop

            while True:
                print("Please choose a genre for the book: ") #ask user for the book genre
                if genre_dict: #ensure there are already genres in the genre dictionary
                    genre_choice = input("Please input the genre of the book you're adding to the library: ").strip() #get chosen genre from operator
                    found = False
                    for stored_genre in genre_dict.values():
                        if genre_choice == stored_genre.getname(): #check that the user input is in genre dictionary
                            genre_choice = gu.get_genre_id(genre_choice)
                            found = True
                            break
                    if found:
                        #Execute query
                        cursor.execute(query, (title, genre_choice, author, isbn, db_date))
                        conn.commit()
                        book_temp = Book(title, genre_choice, author, isbn, pub_date)
                        book_dict[book_temp.get_book_id()] = book_temp
                        print(f'Book "{book_temp.get_title()}" was added successfully')
                        break
                    else:
                        print(f"The genre {genre_choice} is not in the avilable list of genres.")
                        choice_to_add = input("Do you want to add the genre to the list? (yes/no): ")
                        if choice_to_add.lower() == 'yes' or 'y':
                            gu.add_genre(genre_dict)
                else: 
                    print("There are no genres added to the library currently. Please add genre to continue adding book.") #notify operator and ask them to add genre to dictionary
                    gu.add_genre(genre_dict) #add genre to the genre dictionary then continue loop
        
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

def borrow_book(user_dict, book_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to add the book to the Books table
            query = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
            
            while True:
                try:
                    #get necessary information from operator
                    user = input("Please enter the Name or Library ID of the user checking out the book: ")
                    book = input("Please enter the title of the book you'd like to borrow: ")
                    today = dt.date.today()
                    return_delta = dt.timedelta(days=14)
                    borrow_date = today.strftime("%Y-%m-%d")
                    return_date = (today + return_delta).strftime("%Y-%m-%d") 

                    #ensure all inputs are converted to ids for db handling
                    if not user.isnumeric(): #check if input is not the Library ID
                        user = uu.get_user_id_from_name(user_dict, user) #get Library ID
                    else:
                        if uu.get_user_id_from_library_id(book):
                            user = uu.get_user_id_from_library_id(book)
                        else:
                            raise Exception("Input Library ID was not found")
                    if book_dict[book].get_availability():
                        cursor.execute(query,(user, book, borrow_date, return_date))
                        conn.commit()
                        book_dict[book].set_borrowed()
                        print(f'"{book_dict[book].get_title()}" has been successfully borrowed by user {user_dict[user].get_name()} please retun by or on {return_date}') #notify operator of success of borrowing title
                        break
                    else: #status borrowed
                        print(f'"{book_dict[book].get_title()}" is already borrowed out') #notify operator that that book is unavailable
                        break
                except KeyError: #key error occurs
                    print("\033[7mInvalid Input: Please try again\033[0m") #Notify operator of error
                except Exception as ex:
                    print(f"\033[7mInvalid Input: {ex}: Please try again\033[0m")

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

def return_book(user_dict, book_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to add the book to the Books table
            query = "DELETE FROM borrowed_books WHERE user_id = %s AND book_id =  %s"
            
            while True:
                try:
                    #get necessary information from operator
                    user = input("Please enter the Name or Library ID of the user checking out the book: ")
                    book = input("Please enter the title of the book you'd like to borrow: ")
                    
                    #ensure all inputs are converted to ids for db handling
                    if not user.isnumeric(): #check if input is not the Library ID
                        user = uu.get_user_id_from_name(user_dict, user) #get Library ID
                    else:
                        if uu.get_user_id_from_library_id(book):
                            user = uu.get_user_id_from_library_id(book)
                        else:
                            raise Exception("Input Library ID was not found")
                    if book_dict[book].get_availability():
                        cursor.execute(query,(user, book))
                        conn.commit()
                        book_dict[book].set_available()
                        print(f'"{book_dict[book].get_title()}" has been successfully returned by user {user_dict[user].get_name()}') #notify operator of success of borrowing title
                        break
                    else: #status borrowed
                        print(f'"{book_dict[book].get_title()}" is already borrowed out') #notify operator that that book is unavailable
                        break
                except KeyError: #key error occurs
                    print("\033[7mInvalid Input: Please try again\033[0m") #Notify operator of error
                except Exception as ex:
                    print(f"\033[7mInvalid Input: {ex}: Please try again\033[0m")

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

def display_book(book_dict, book_id):
    try:
        if book_id in book_dict.keys():
            print(f"\n Title: {book_dict[book_id].get_title()}")
            print(f"Author {book_dict[book_id].get_author()}")
            print(f"Genre: {book_dict[book_id].get_name()}")
            print(f"ISBN: {book_dict[book_id].get_isbn()}")
            print(f"Publication Date: {book_dict[book_id].get_publication_date().strftime("%B %d, %Y")}")
            available = book_dict[book_id].get_status()
            available = 'Available' if available else 'Borrowed out'
            print(f"Availability: {available}\n")
        else:
            raise KeyError("The book chosen to be displayed does not exist")
    except KeyError as ke:
        print(f"\033[7m{ke}[0m")

def search_books(book_dict, author_dict):
    while True:
        #Seach criteria menu
        choice = input("\nCriteria to search with:\n1. Search by Book Title\n2. Search by Book Author\n3. Search by ISBN\n4. Search by Genre\n5. Return to previous menu\nWhich criteria would you like to search for a book by?: ").strip()

        #search by title
        if choice == '1': 
            book_title = input("Please input the title you are searching for: ").strip() #get title to search from operator
            book_id = book_id_from_title(book_dict, book_title) #convert title to isbn
            display_book(book_dict, book_id) #display the title chosen by the operator
            break #end loop
               
        #search by author
        elif choice == '2': 
            author = input("What is the name of the Author you'd like to search for books from?").strip() #get author to search from operator
            found_list = get_books_by_author(book_dict, get_author(author_dict, book_dict, author)) #initialize list of found books

            if found_list:
                #one result
                if len(found_list) == 1:
                    display_book(book_dict, found_list[0])

                #multiple results
                elif len(found_list) > 1: #titles found and more than one
                    print(f"Titles available from author {author}:") #heading for found titles
                    counter = 1
                    for book in found_list: #iterate found books
                        print(f'"{counter}: {book_dict[book].get_title()}", ISBN: {book_dict[book].get_isbn()}')
                        counter += 1
                    while True:
                        book_choice = int(input("Please enter the number of the title you wish to view: ").strip()) #ask to choose a title
                        if book_choice > 0 and book_choice <= len(found_list):
                            display_book(book_dict, book_choice, found_list[choice - 1])
                            break
                        else: #invalid choice
                            print("That was not a valid choice. Please try again")
                    
            #none found
            else:
                print("There were no books by that author found in the library")
                break
        
        #search isbn
        elif choice == '3':
            isbn_search = input("Please input the ISBN of the title you're searching for: ").strip() #get ISBN from operator
            display_book(book_dict, book_id_from_isbn(isbn_search))
        
        elif choice == '4': #seach by Genre
            genre_search = input("Please enter the genre you'd like to search for: ").strip()
            found = gu.get_books_from_genre(genre_search)
            if found:
                if len(found) == 1: #check that titles found and there is only one
                    display_book(found[0]) #display book in list
                elif len(found) > 1:
                    print(f"Titles available in genre {genre_search}:") #heading for found titles
                    #print titles
                    counter = 1
                    for book in found:
                        print(f'{counter}: {book_dict[book].get_title()}') 
                    while True:
                        book_choice = int(input("Please enter the number of the title you wish to view: ").strip())
                        if book_choice < 0 and book_choice >= len(found):
                            display_book(book_dict, found[book_choice - 1])
                        else:
                            print("Invalid choice, please input a valid option")

            else: #none found
                print(f"There were no books found in the genre {genre_search}")

        #leave
        elif choice == '5':
            break
        
        else:
            print("That was an invalid choice. Please try again")

def display_all_books(book_dict):
    if book_dict:
        print("\n\033[4mBooks in the library:\033[0m")
        for book in book_dict.values(): #iterate through book dictionary
            print(f"Title: {book.get_title()}")
            print(f"Author {book.get_author()}")
            print(f"Genre: {book.get_name()}")
            print(f"ISBN: {book.get_isbn()}:")
            print(f"Publication Date: {book.get_publication_date().strftime("%Y-%m-%d")}")
            print(f"Status: {book.get_status()}\n")
    else:
        print("There are no books currently in the library\n")

def get_books_by_author(book_dict, author_id):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Books title WHERE author_id = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (author_id,))
            
            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and how many results come back
            if results:
                return_value = []
                for value in results:
                    return_value.append(value[0])           
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
        
def book_id_from_isbn(book_dict, author_dict, isbn): #function to return the isbn of a book by its title
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Books id WHERE isbn = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (isbn,))
            
            #store result for manipulation
            results = cursor.fetchone()

            #check that results come back and how many results come back
            if results:
                    return_value = results[0]
            else:
                raise Error("That title was not found")
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

def load_books_from_db(book_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT * FROM books" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query)

            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and how many results come back
            if results:
                for result in results:
                    id, title, author_id, genre_id, isbn, publication_date, availability = result

                    book_dict[id] = Book(title, author_id, genre_id, isbn, publication_date, availability)
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