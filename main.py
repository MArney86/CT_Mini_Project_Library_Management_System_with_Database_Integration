import book_utils as bu
import author_utils as au
import genre_utils as gu
import user_utils as uu
from connect_mysql import establish_db
import sys

library_books = {}
library_users = {}
library_authors = {}
library_genres = {}

def main():
    establish_db()
    gu.load_genres_from_db(library_genres)
    au.load_authors_from_db(library_authors)
    uu.load_users_from_db(library_users)
    bu.load_books_from_db(library_books)

    while True:
        #display Main Menu
        print("\nWelcome to the Library Management System!\n") 
        print("Main Menu:")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Genre Operations")
        print("5. Quit")

    
        choice = input("What would you like to do? ").strip()
        #Book Menu
        if choice == '1':
            book_menu()
        #User Menu
        elif choice == '2':
            user_menu() 
        #Author Menu
        elif choice == '3':
            author_menu() 
        #Genre Menu
        elif choice == '4': 
            genre_menu()
        #Quit
        elif choice == '5': #chose to quit
            sys.exit("Thank you for using the Library Management System") 
        #invalid input
        else:
            print("\033[7mInvalid choice. Please try again.\033[0m")
            
def book_menu():
    while True:
        #Display menu
        print("\nBook Operations:")
        print("1. Add a new book")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Search for a book")
        print("5. Display all books")
        print("6. Return to previous menu")

        choice = input("What would you like to do?: ")

        #Add book
        if choice == '1':
            bu.add_book(library_books, library_genres, library_authors)
        #borrow book    
        elif choice == '2':
            bu.borrow_book(library_users, library_books, library_authors)
        #return a book
        elif choice == '3':
            bu.return_book(library_users, library_books, library_authors)
        #search for a book
        elif choice == '4':
            bu.search_books(library_books,library_authors)
        #display all books
        elif choice == '5': 
            bu.display_all_books(library_books)
        #Leave
        elif choice == '6': 
            break
        #invalid input
        else:
            print("\033[7mInvalid choice. Please try again.\033[0m")


def user_menu():
    while True:
        #Display Menu
        print("\nUser Operations:")
        print("1. Add a new user")
        print("2. View user details")
        print("3. Display all users")
        print("4. Return to previous menu")

        choice = input("What would you like to do?: ").strip() #get user choice
        
        #Add user
        if choice == '1': 
            uu.add_user(library_users)
        #View user
        elif choice == '2':
            uu.view_user_details(library_users, library_books)
        #Display all users
        elif choice == '3':
            uu.display_all_users(library_users, library_books)
        #Leave
        elif choice == '4':
            break
        #Invalid input
        else:
            print("\033[7mInvalid choice. Please try again.\033[0m")

def author_menu():
    while True:
        #Display menu
        print("\nAuthor Operations:")
        print("1. Add a new author")
        print("2. View author details")
        print("3. Display all authors")
        print("4. Return to previous menu")

        choice = input("What would you like to do?: ").strip()
        
        #Add author
        if choice == '1':
            au.add_author(library_authors)
        #View author
        elif choice == '2':
            au.view_author_details(library_authors, library_books)
        #View all authors
        elif choice == '3':
            au.display_all_authors(library_authors) 
        #Leave
        elif choice == '4': 
            break
        #invalid input 
        else: 
            print("\033[7mInvalid choice. Please try again.\033[0m")

def genre_menu():
    while True:
        print("\nGenre Operations:")
        print("1. Add a new genre")
        print("2. View genre details")
        print("3. Display all genres")
        print("4. Return to previous menu")

        choice = input("What would you like to do?: ").strip()

        #add genre
        if choice == '1':
            gu.add_genre(library_genres)
        #view genre
        elif choice == '2':
            gu.view_genre_details(library_genres)
        #view all genres
        elif choice == '3':
            gu.display_all_genres(library_genres)
        #Leave
        elif choice == '4':
            break
        #invalid input
        else: 
            print("\033[7mInvalid choice. Please try again.\033[0m")

if __name__ == "__main__":
    main()