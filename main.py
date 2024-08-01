import book_utils as bu
import author_utils as au
import genre_utils as gu
import user_utils as uu
import files_handler as fh
import sys

library_books = {}
library_users = {}
library_authors = {}
library_genres = {}

file_support = fh.File_Handler('users.log', 'genres.log', 'books.log', 'authors.log')
file_support.load_all(library_authors, library_books, library_genres, library_users)

def main():
    while True: #loop in case of invalid input
        print("\nWelcome to the Library Management System!\n") #display main menu
        print("Main Menu:")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Genre Operations")
        print("5. Quit")

    
        choice = input("What would you like to do? ").strip() #get user's choice
        if choice == '1': #chose book operations
            book_menu() #load the book menu
        elif choice == '2': #chose user operations
            user_menu() #load the user menu
        elif choice == '3': #chose author operations
            author_menu() #load the author menu
        elif choice == '4': #chose genre operations
            genre_menu() #load the genre menu
        elif choice == '5': #chose to quit
            file_support.save_all(library_authors, library_books, library_genres, library_users) #save all information to file
            sys.exit("Thank you for using the Library Management System") #exit program to system/terminal prompt
        elif choice == 'Force Reload':
            file_support.reload_all(library_authors, library_books, library_genres, library_users) #clear and reload all information from file
            print("\033[7mAll information has been cleared and reloaded from file\033[0m") #notification of reload
        elif choice == 'Force Save':
            file_support.save_all(library_authors, library_books, library_genres, library_users) #force save all information to file
            print("\033[7mAll information has been saved to file by operator request\033[0m") #notification of forced save
        else: #invalid response
            print("Invalid choice. Please try again.") #notify user of invalid response
            
def book_menu():
    while True: #loop in case of invalid input
        print("\nBook Operations:") #display book operations menu
        print("1. Add a new book")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Search for a book")
        print("5. Display all books")
        print("6. Return to previous menu")

        choice = input("What would you like to do?: ") #get user choice
        if choice == '1': #chose to add book
            key, genre_bool, genre = bu.add_book(library_books, library_genres) #add book and store returned key and info about whether genres were updated
            file_support.update_books(library_books, key) #save new entry to file
            if genre_bool: #if genres were updated during book addition
                file_support.update_genres(library_genres, genre) #save new genre to file as well

        elif choice == '2': #chose to borrow a book
            success = bu.borrow_book(library_users, library_books) #borrow book
            if success: #if borrow successful
                file_support.save_books(library_books) #save books with updated information
                file_support.save_users(library_users) #save users with updated information
        elif choice == '3': #chose to return a book
            success = bu.return_book(library_users, library_books) #return book
            if success: #if return successful
                file_support.save_books(library_books) #save books with updated information
                file_support.save_users(library_users) #save users with updated information
        elif choice == '4': #chose to search for a book
            bu.search_books(library_books) #search books
        elif choice == '5': #chose to display all books
            bu.display_all_books(library_books) #display all books
        elif choice == '6': #chose to leave
            break #end loop and function
        else: #invalid response
            print("Invalid choice. Please try again.") #notify user of invalid response


def user_menu():
    while True: #loop in case of invalid input
        print("\nUser Operations:")
        print("1. Add a new user")
        print("2. View user details")
        print("3. Display all users")
        print("4. Return to previous menu")

        choice = input("What would you like to do?: ").strip() #get user choice
        if choice == '1': #chose to add user
            key = uu.add_user(library_users) #add user
            file_support.update_users(library_users, key) #save new user to file
        elif choice == '2': #view a user's details
            uu.view_user_details(library_users, library_books) #view user details
        elif choice == '3': #display all users
            uu.display_all_users(library_users, library_books) #display all users
        elif choice == '4': #chose to leave
            break #end loop and function
        else: #invalid response
            print("Invalid choice. Please try again.") #notify user of invalid response

def author_menu():
    while True: #loop in case of invalid input
        print("\nAuthor Operations:")
        print("1. Add a new author")
        print("2. View author details")
        print("3. Display all authors")
        print("4. Return to previous menu")

        choice = input("What would you like to do?: ").strip() #get user choice
        if choice == '1': #chose to add user
            key = au.add_author(library_authors) #add user
            file_support.update_authors(library_authors, key) #save new author to file
        elif choice == '2': #view a user's details
            au.view_author_details(library_authors) #view user details
        elif choice == '3': #display all users
            au.display_all_authors(library_authors) #display all users
        elif choice == '4': #chose to leave
            break #end loop and function
        else: #invalid response
            print("Invalid choice. Please try again.") #notify user of invalid response

def genre_menu():
    while True: #loop in case of invalid input
        print("\nGenre Operations:")
        print("1. Add a new genre")
        print("2. View genre details")
        print("3. Display all genres")
        print("4. Return to previous menu")

        choice = input("What would you like to do?: ").strip() #get user choice
        if choice == '1': #chose to add genre
            key = gu.add_genre(library_genres) #add genre
            file_support.update_genres(library_genres, key) #save new genre to file
        elif choice == '2': #view a genre's details
            gu.view_genre_details(library_genres) #view genre details
        elif choice == '3': #display all genres
            gu.display_all_genres(library_genres) #display all genres
        elif choice == '4': #chose to leave
            break #end loop and function
        else: #invalid response
            print("Invalid choice. Please try again.") #notify user of invalid response

if __name__ == "__main__":
    main()