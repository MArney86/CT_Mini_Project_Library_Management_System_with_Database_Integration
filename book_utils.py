from book import Book
import genre_utils as gu
import datetime as dt
import user_utils as uu
from author_utils import get_author
from connect_mysql import connect_database
from mysql.connector import Error



def book_id_from_title(book_dict, author_dict, title,):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to select the id of the book matching the input title
            query = "SELECT id FROM books WHERE title = %s"

            #Execute query and store results
            cursor.execute(query, (title,))
            results = cursor.fetchall()

            #check that results come back and how many results come back
            if results:
                #one result
                if len(results) == 1:
                    return_value = results[0][0]
                
                #multiple results and print them out to choose the specific one wanted
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
                            return_value = results[choice - 1][0]
                        else:
                            print("That was not a valid choice. Please try again")
            #no results
            else:
                return_value = None
                print("That title was not found")
        
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
            return return_value
    
def is_valid_date(user_date):
    #initialize return value
    result = True

    #attempt to break up date string and add as date class
    try: 
        year_str, month_str, day_str = user_date.split('-')
        try: 
            dt.date(year = int(year_str), month = int(month_str), day = int(day_str)) 
        except ValueError: 
            result = False
    except ValueError:
        result = False 

    return result

def add_book(book_dict, genre_dict, author_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to add the book to the Books table
            query = "INSERT INTO Books (title, genre_id, author_id, isbn, publication_date) VALUES (%s, %s, %s, %s, %s)"

            #get book information from operator
            title = input("Please enter the title of the book you'd like to add: ").strip()
            author = get_author(author_dict, book_dict, input("Please enter the Author of the book you'd like to add: ").strip())
            isbn = input("Please enter the ISBN for the book you'd like to add: ").strip()

            #get publication date from operator and verify it asking to try again if invalid
            while True:
                pub_date = input("Please enter the publication date of the book you'd like to add (YYYY-MM-DD format): ").strip()
                if is_valid_date(pub_date):
                    db_date = pub_date
                    year_str, month_str, day_str = pub_date.split('-')
                    pub_date = dt.date(year = int(year_str), month = int(month_str), day = int(day_str))
                    break
                else:
                    print("Invalid date, please try again")

            #get genre from operator and verify it against existing genres for id if genres in db an then adding book to db and dictionary or prompting to add genre then repeating block to add book
            while True:
                print("Please choose a genre for the book: ")
                if genre_dict:
                    genre_choice = input("Please input the genre of the book you're adding to the library: ").strip()
                    found = False
                    #check for genre in dictionary and change genre variable to id
                    for stored_genre in genre_dict.values():
                        if genre_choice == stored_genre.get_name():
                            genre_choice = gu.get_genre_id(genre_choice)
                            found = True
                            break
                    if found:
                        #Execute query
                        cursor.execute(query, (title, genre_choice, author, isbn, db_date))
                        conn.commit()
                        #add book to dictionary
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
                    print("There are no genres added to the library currently. Please add genre to continue adding book.")
                    gu.add_genre(genre_dict)
        
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

def borrow_book(user_dict, book_dict, author_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to add the book to the borrowed_books table
            query = "INSERT INTO borrowed_books (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)"
            
            while True:
                try:
                    #get necessary information from operator
                    user = uu.get_user_id_from_name(user_dict, input("Please enter the Name of the user checking out the book: ").strip())
                    book = input("Please enter the title of the book you'd like to borrow: ").strip()
                    
                    #get todays date as borrow date and calculate return date 2 weeks from borrow
                    today = dt.date.today()
                    return_delta = dt.timedelta(days=14)
                    borrow_date = today.strftime("%Y-%m-%d")
                    return_date = (today + return_delta).strftime("%Y-%m-%d") 

                    #get book id
                    book = book_id_from_title(book_dict, author_dict, book)

                    #verify that book is available and add to borrow list if it is otherwise notify user
                    if book_dict[book].get_availability():
                        #execute query
                        cursor.execute(query,(user, book, borrow_date, return_date))
                        conn.commit()
                        #set borrowed in book dictionary
                        book_dict[book].set_borrowed()
                        print(f'"{book_dict[book].get_title()}" has been successfully borrowed by user {user_dict[user].get_name()} please return by or on {return_date}')
                        break
                    
                    else:
                        print(f'"{book_dict[book].get_title()}" is already borrowed out')
                        break
                except KeyError:
                    print("\033[7mInvalid Input: Please try again\033[0m")
                except Exception as ex:
                    print(f"\033[7mInvalid Input: {ex}: Please try again\033[0m")

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

def return_book(user_dict, book_dict, author_dict):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query to remove the book from the borrowed books table
            query = "DELETE FROM borrowed_books WHERE user_id = %s AND book_id = %s"
            
            while True:
                try:
                    #get necessary information from operator
                    user = input("Please enter the Name or Library ID of the user who checked out the book: ")
                    book = input("Please enter the Title of the book you'd like to return: ")
                    
                    #ensure all inputs are converted to ids for db handling
                    if not user.isnumeric():
                        user = uu.get_user_id_from_name(user_dict, user)
                    else:
                        if uu.get_user_id_from_library_id(book):
                            user = uu.get_user_id_from_library_id(book)
                        else:
                            print("Input Library ID was not found")
                            continue
                    book = book_id_from_title(book_dict, author_dict, book)
                    #check that book is actually borrowed out then remove from db and change book settings
                    if book_dict[book].get_availability():
                        #execute query
                        cursor.execute(query,(user, book))
                        conn.commit()
                        #change book in dictionary
                        book_dict[book].set_available()
                        print(f'"{book_dict[book].get_title()}" has been successfully returned by user {user_dict[user].get_name()}') 
                        break
                    else: #status available
                        print(f'"{book_dict[book].get_title()}" is not borrowed out')
                        break

                #exceptions
                except KeyError:
                    print("\033[7mInvalid Input: Please try again\033[0m")
                except Exception as ex:
                    print(f"\033[7mInvalid Input: {ex}: Please try again\033[0m")
        
        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("\033[7mError: Value for name is too long.\033[0m")
            else:
                print(f"\033\7mError: {e}\033[0m")
        
        #close connections
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

def display_book(book_dict, author_dict, book_id):
    #display the information of the book whose id was input
    try:
        if book_id in book_dict.keys():
            print(f"\n Title: {book_dict[book_id].get_title()}")
            print(f"Author {author_dict[book_dict[book_id].get_author()].get_name()}")
            print(f"Genre: {book_dict[book_id].get_genre()}")
            print(f"ISBN: {book_dict[book_id].get_isbn()}")
            print(f"Publication Date: {book_dict[book_id].get_publication_date().strftime("%B %d, %Y")}")
            available = book_dict[book_id].get_availability()
            available = 'Available' if available else 'Borrowed out'
            print(f"Availability: {available}\n")
        else:
            print("The book chosen to be displayed does not exist")
    
    #exceptions
    except KeyError as ke:
        print(f"\033[7m{ke}\033[0m")

def search_books(book_dict, author_dict):
    while True:
        #Seach criteria menu
        choice = input("\nCriteria to search with:\n1. Search by Book Title\n2. Search by Book Author\n3. Search by ISBN\n4. Search by Genre\n5. Return to previous menu\nWhich criteria would you like to search for a book by?: ").strip()

        #search by title
        if choice == '1': 
            book_title = input("Please input the title you are searching for: ").strip()
            book_id = book_id_from_title(book_dict, author_dict, book_title)
            display_book(book_dict, author_dict, book_id)
            break #end loop
               
        #search by author
        elif choice == '2': 
            author = input("What is the name of the Author you'd like to search for books from?").strip() 
            found_list = get_books_by_author(get_author(author_dict, book_dict, author))

            if found_list:
                #one result
                if len(found_list) == 1:
                    display_book(book_dict, author_dict, found_list[0])

                #multiple results display results and ask to choose distinct result 
                elif len(found_list) > 1:
                    print(f"Titles available from author {author}:")
                    counter = 1
                    for book in found_list:
                        print(f'"{counter}: {book_dict[book].get_title()}", ISBN: {book_dict[book].get_isbn()}')
                        counter += 1
                    while True:
                        book_choice = int(input("Please enter the number of the title you wish to view: ").strip())
                        if book_choice > 0 and book_choice <= len(found_list):
                            display_book(book_dict, author_dict, found_list[choice - 1])
                            break
                        else: 
                            print("That was not a valid choice. Please try again")
                    
            #none found
            else:
                print("There were no books by that author found in the library")
                break
        
        #search isbn
        elif choice == '3':
            #get isbn from user and display using helper function to get book id from isbn
            isbn_search = input("Please input the ISBN of the title you're searching for: ").strip() #get ISBN from operator
            display_book(book_dict, author_dict, book_id_from_isbn(isbn_search))
        
        #search by genre
        elif choice == '4':
            #get genre from operator and get books within that genre
            genre_search = input("Please enter the genre you'd like to search for: ").strip()
            found = gu.get_books_from_genre(genre_search)

            #check that there are books in that genre
            if found:
                #one result:
                if len(found) == 1:
                    display_book(book_dict, author_dict, found[0])
                #multiple results and choose distinct title searching for
                elif len(found) > 1:
                    print(f"Titles available in genre {genre_search}:")
                    #print titles
                    counter = 1
                    for book in found:
                        print(f'{counter}: {book_dict[book].get_title()}') 
                    #ask to choose specific title
                    while True:
                        book_choice = int(input("Please enter the number of the title you wish to view: ").strip())
                        if book_choice < 0 and book_choice >= len(found):
                            display_book(book_dict, author_dict, found[book_choice - 1])
                        else:
                            print("Invalid choice, please input a valid option")

            #no books in that genre
            else:
                print(f"There were no books found in the genre {genre_search}")

        #leave
        elif choice == '5':
            break
        
        #invalid input
        else:
            print("That was an invalid choice. Please try again")

def display_all_books(book_dict):
    #verify that there are books in dictionary
    if book_dict:
        #print out books and their information
        print("\n\033[4mBooks in the library:\033[0m")
        for book in book_dict.values(): #iterate through book dictionary
            print(f"Title: {book.get_title()}")
            print(f"Author {book.get_author()}")
            print(f"Genre: {book.get_genre()}")
            print(f"ISBN: {book.get_isbn()}:")
            print(f"Publication Date: {book.get_publication_date().strftime("%Y-%m-%d")}")
            print(f"Status: {book.get_availability()}\n")
    #no books in library
    else:
        print("There are no books currently in the library\n")

def get_books_by_author(author_id):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query got get books from input author
            query = "SELECT id FROM books WHERE author_id = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (author_id,))
            
            #store result for manipulation
            results = cursor.fetchall()

            #check that results come back and package them for returning
            return_value = []
            if results:
                for value in results:
                    return_value.append(value[0])
            #no results return None
            else:
                return_value = None

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
            return return_value
        
def book_id_from_isbn(isbn):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT id FROM books WHERE isbn = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (isbn,))
            
            #store result for manipulation
            results = cursor.fetchone()

            #check that results come back and how many results come back
            if results:
                    return_value = results[0]
            else:
                return_value = None
                raise Error("That title was not found")
        #exceptions
        except Error as e:
            if e.errno == 1406:
                print("\033[7mError: Value for name is too long.\033[0m")
            else:
                print(f"033[7mError: {e}\033[0m") #general error

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

            #SQL Query to return all books
            query = "SELECT * FROM books"

            #Execute query and store results
            cursor.execute(query)
            results = cursor.fetchall()

            #check that results came back and add them to the book dictionary
            if results:
                for result in results:
                    id, title, author_id, genre_id, isbn, publication_date, availability = result
                    book_dict[id] = Book(title, author_id, genre_id, isbn, publication_date, bool(availability))
            #no books in db
            else:
                raise Error("There are currently no Books in the database")

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