import Book
import genre_utils as gu
import datetime as dt
import user_utils as uu
from connect_mysql import connect_database
from mysql.connector import Error



def isbn_from_title(book_dict, title): #function to return the isbn of a book by its title
    found = False #initialize found flag
    found_list = [] #initialize list of books with the searched title
    for isbn, book in book_dict.items(): #iterate through the books in the book dictionary
        if book.get_title().lower() == title.lower(): #check title of iterated book ignoring capitalization
            found = True #set found flag to True
            found_list.append(isbn) #add isbn of found book to found list
        else: #no match
            continue #continue loop
    if found and len(found_list) == 1: #test if books found and there is only one in the list
        return found_list[0] #return value of isbn from found book
    elif found and len(found_list) > 1: #test if books are found and there are more than 1
        print(f"\nBooks with title {title} found:") #iterate through found books
        counter = 1 #counter to keep track of location for user choice 
        for book in found_list: #iterate through found list
            print(f'{counter}.: "{book_dict[book].get_title()}" by {book_dict[book].get_author()} published on {book_dict[book].get_publication_date().strftime("%B %d, %Y")}') #print details of book for user to choose from
            counter += 1 #update counter
        while True: #loop in case of invalid inputs
            choice = input(f'Please choose the number of the particular book with title "{title}" you were looking for') #ask user for their choice
            try: #error handling
                if int(choice) > 0 and int(choice) <= len(found_list): #verify valid choice
                    return found_list[int(choice) - 1] #return chosen isbn
                else: #invalid choice
                    print("That was not a valid choice. Please try again") #notify operator of invalid choice
            except TypeError: #invalid input type error
                print("\033[7mOnly inputs of the number of your choice accepted. Please try again\033[0m") #notify operator of error
            except ValueError: #nonsensical number input error
                print("\033[7mThat input does not map to a number. Please try again\033[0m") #notify operator of error
            except Exception: #general exception
                print("\033[7mUnexpect error occurred. Please try again\033[0m") #notify operator of error
    else: #no books found
        print("That title has returned no matching books") #notify operator that book is not found
        return False
    
def is_valid_date(user_date): #function to validate date inputs
    result = True #initialize returned value to true

    try: #error handling
        month_str, day_str, year_str = user_date.split('/') #split input date
        try: #more error handling
            dt.date(year = int(year_str), month = int(month_str), day = int(day_str)) #attempt to add values to a date object
        except ValueError: #value error from date() attempt
            result = False #return value of false
    except ValueError: #value error from split attempt
        result = False #return value of false

    return result #no errors, return true value

def add_book(book_dict, genre_dict):
    title = input("Please enter the title of the book you'd like to add: ").strip() #get title from operator
    author = input("Please enter the Author of the book you'd like to add: ").strip() #get author from operator
    isbn = input("Please enter the ISBN for the book you'd like to add: ").strip() #get isbn from operator

    while True: #loop incase of invalid inputs
        pub_date = input("Please enter the publication date of the book you'd like to add (MM/DD/YYYY format): ").strip() #get publication date from operator
        if is_valid_date(pub_date): #check that input is valid
            month_str, day_str, year_str = pub_date.split('/') #split input date
            pub_date = dt.date(year = int(year_str), month = int(month_str), day = int(day_str)) #add publication date as date object
            break #end loop
        else: #invalid input
            print("Invalid date, please try again") #notify operator and continue loop

    while True: #loop incase of invalid inputs
        print("Please choose a genre for the book: ") #ask user for the book genre
        genre_bool = False
        if genre_dict: #ensure there are already genres in the genre dictionary
            for genre in genre_dict.keys(): #iterate through genre names as keys in genre dictionary
                print(genre_dict[genre].get_name()) #print the iterated genre
            genre_choice = input("Please input the genre of the book you're adding to the library: ").strip() #get chosen genre from operator
            if genre_choice.lower() in genre_dict.keys(): #check that the user input is in genre dictionary
                name = genre_dict[genre_choice.lower()].get_name() #set name placeholder
                description =genre_dict[genre_choice.lower()].get_description() #set descriptor placeholder
                category = genre_dict[genre_choice.lower()].get_category() #set category placeholder
                break #end loop
            else: #chosen genre is not in genre dictionary
                print("That genre isn't in the list of available genres. Please add genre to continue adding book.") #notify operator and ask them to add genre to dictionary
                genre = gu.add_genre(genre_dict) #add genre to the genre dictionary then continue loop
                genre_bool = True
        else: #no genres in dictionary
            print("There are no genres added to the library currently. Please add genre to continue adding book.") #notify operator and ask them to add genre to dictionary
            genre = gu.add_genre(genre_dict) #add genre to the genre dictionary then continue loop
            genre_bool = True

    book_dict[isbn] = Book(name, description, category, title, author, isbn, pub_date) #create new book in book dictionary with isbn as identifier
    return (isbn, genre_bool, genre)


def borrow_book(user_dict, book_dict):
    while True: #loop in case of invalid input
        try: #error handling
            user = input("Please enter the name or Library ID of the user checking out the book: ") #get user name or library id from operator
            query = input("Please enter the ISBN or title of the book you'd like to borrow: ") #get title or isbn of book from operator
    
            if not user.isnumeric(): #check if input is not the Library ID
                user = uu.get_id_from_name(user_dict, user) #get Library ID

            if not query.isnumeric() or (query.isnumeric() and len(query) < 13): #check that input is not the ISBN
                query = isbn_from_title(book_dict, query)
    
            if book_dict[query].get_status() == "Available": #check status of book is available
                user_dict[user].add_borrowed(book_dict, query) #add book to user's borrow list
                book_dict[query].set_status_borrowed()#change book status to borrowed
                print(f'"{book_dict[query].get_title()}" has been borrowed by user {user_dict[user].get_name()}') #notify operator of success of borrowing title
                return True
            else: #status borrowed
                print(f'"{book_dict[query].get_title()}" is already borrowed out') #notify operator that that book is unavailable
                return False
        except KeyError: #key error occurs
            print("\033[7mErroneous Input: Please try again\033[0m") #Notify operator of error

def return_book(user_dict, book_dict):
    while True: #loop in case of erroneous input
        try:#error handling
            user = input("Please enter the name or Library ID of the user who checked out the book: ").strip() #get user name or library id from operator
            query = input("Please enter the ISBN or title of the book you'd like to return: ").strip() #get title or isbn of book from operator
            if not user.isnumeric():
                user = uu.get_id_from_name(user_dict, user)

            if not query.isnumeric() or (query.isnumeric() and len(query) < 13):
                query = isbn_from_title(book_dict, query)

            if book_dict[query].get_status() == "Borrowed": #check status of book is not available
                user_dict[user].remove_borrowed(query) #remove book from user's borrow list
                book_dict[query].set_status_available()#change book status to available
                print(f'"{book_dict[query].get_title()}" has been returned by user {user_dict[user].get_name()}') #notify operator of success of returning title
                return True
            else: #status available
                print(f'"{book_dict[query].get_title()}" is already returned/available') #notify operator that that book is already returned/available
                return False
        except KeyError: #KeyError Occurs
            print("\033[7mErroneous Input: Please try again\033[0m") #Notify operator of error

def display_book(book_dict, isbn):
    try:
        if isbn in book_dict.keys():
            print(f"\n Title: {book_dict[isbn].get_title()}")
            print(f"Author {book_dict[isbn].get_author()}")
            print(f"Genre: {book_dict[isbn].get_name()}")
            print(f"ISBN: {book_dict[isbn].get_isbn()}")
            print(f"Publication Date: {book_dict[isbn].get_publication_date().strftime("%B %d, %Y")}") #print book data to operator
            print(f"Status: {book_dict[isbn].get_status()}\n")
        else:
            print("\nThe title chosen to display does not exist\n")
    except KeyError:
        print("\033[7mInvalid Book ID\033[0m")

def search_books(book_dict):
    while True: #loop in case of invalid input
        choice = input("\nSearch criteria choices:\n1. By Book Title\n2. By Book Author\n3. By ISBN\n4. By Genre\n5. Return to previous menu\nWhich criteria would you like to search for a book by?: ").strip() #ask user what criteria they want to search
        
        if choice == '1': #search by title
            query = input("Please input the title you are searching for: ").strip() #get title to search from operator
            query = isbn_from_title(book_dict, query) #convert title to isbn
            display_book(book_dict, query) #display the title chosen by the operator
            break #end loop
        
        elif choice == '2': #search by author
            query = input("What is the name of the Author you'd like to search for books from?").strip() #get author to search from operator
            found = False #initialize found flag
            found_list = [] #initialize list of found books
            for isbn, book in book_dict.items(): #iterate through books in dictionary
                if  query.lower() == book.get_author().lower():#check that author matches
                    found = True #set found flag to true
                    found_list.append(isbn) #add isbn to found list
                else: #author doesn't match
                    continue #continue
            if found and len(found_list) == 1: #check that titles found and there is only one
                display_book(book_dict, found_list[0])
            elif found and len(found_list) > 1: #titles found and more than one
                print(f"Titles available from author {query}:") #heading for found titles
                for book in found_list: #iterate found books
                    print(f'"{book_dict[book].get_title()}" by {book_dict[book].get_author()}, ISBN: {book_dict[book].get_isbn()}') #print title with attributed authors and isbn 
                book_choice = input("Please enter the ISBN of the title you wish to view: ").strip() #ask to choose a title
                display_book(book_dict, book_choice) #display the chose title
            else: #none found
                print("There were no books by that author found in the library") #notify operator of author not being found
        
        elif choice == '3': #search isbn
            query = input("Please input the ISBN of the title you're searching for: ").strip() #get ISBN from operator
            display_book(book_dict, query) #display_book(isbn)
        
        elif choice == '4': #seach by Genre
            query = input("Please enter the genre you'd like to search for: ").strip()
            found = False #found flag initialized to false
            found_list = [] #found list initialized
            for isbn, book in book_dict.items():#iterate through books
                if book.get_name().lower() == query.lower(): #check for genre name in book
                    found = True#set found flag to true
                    found_list.append(isbn)#add isbn to found list
                else: #no match
                    continue #continue
            if found and len(found_list) == 1: #check that titles found and there is only one
                display_book(found_list[0]) #display book in list
            elif found and len(found_list) > 1:
                print(f"Titles available in genre {query}:") #heading for found titles
                for book in found_list: #iterate found books
                    print(f'"{book_dict[book].get_title()}" by {book_dict[book].get_author()}, ISBN: {book_dict[book].get_isbn()}') #print title with attributed authors and isbn 
                book_choice = input("Please enter the ISBN of the title you wish to view: ").strip() #ask to choose a title
                display_book(book_dict, book_choice) #display the chose title#print list of titles with attributed authors and isbn to choose title
            else: #none found
                print(f"There were no books found in the genre {query}")

        elif choice == '5': #leave
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
            print(f"Publication Date: {book.get_publication_date().strftime("%B %d, %Y")}") #print book data to operator#display_book(isbn key)
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
                return_value = results
            
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
    
def get_book_id_from_db(title, author_id, publication_date):
    #establish connection
    conn = connect_database()

    #ensure connection
    if conn is not None:
        try:
            #establish cursor
            cursor = conn.cursor()

            #SQL Query
            query = "SELECT FROM Books id WHERE title = %s AND publication_date = %s AND author_id = %s" #inserts new member in the Members table using the information passed to the function

            #Execute query
            cursor.execute(query, (title, publication_date, author_id))
            
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