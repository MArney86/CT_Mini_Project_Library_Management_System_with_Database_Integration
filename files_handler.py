import book_utils as bu
import author_utils as au
import genre_utils as gu
import user_utils as uu
import datetime as dt
import os
import sys

class File_Handler():
    def __init__(self, user_file, genre_file, book_file, author_file):
        self._user_path = user_file
        self._genre_path = genre_file
        self._book_path = book_file
        self._author_path = author_file

    def save_genres(self, genres_dict):
        while True: #loop to retry if file error
            try: #error handling for file opening
                with open(self._genre_path,"w") as genrefile: #open genre.log as genrefile
                    lines = [] #create empty list of lines
                    for key, genre in genres_dict.items(): #iterate through entries in genres dictionary
                        temp = f'{key}::{genre.get_name()}::{genre.get_description()}::{genre.get_category()}\n' #build line from genre class values
                        lines.append(temp) #add line to list of lines
                    try: #error handling for write
                        genrefile.writelines(lines) #write generated lines to file
                        break #break loop and leave function
                    except (IOError, OSError): #catch IOErrors
                        print("\033[7mUnexpected IOError: attempt file access again?\033[0m") #notify operator of error
                        choice = input("(yes/no): ") #get choice from user
                        if choice == 'yes' or 'y':#check that user chose retry
                            continue #go back to start of loop
                        else: #user chose no
                            print("\033[7mUnable to save genres.\033[0m") #notify user of failure
                            break#end loop
            except (FileNotFoundError, PermissionError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._genre_path} to save genres.\033[0m") #notify user of failure
                    break #end loop


    def save_books(self, books_dict):
        while True: #loop for error handling
            try: #error handling for opening file
                with open(self._book_path,"w") as bookfile: #open book.log as bookfile
                    lines = [] #empty lines list
                    for key, book in books_dict.items(): #iterate through the book dictionary
                        temp = f'{key}::{book.get_title()}::{book.get_author()}::{book.get_isbn()}::{book.get_publication_date().strftime("%Y/%m/%d")}::{book.get_status()}::{book.get_name()}\n' #get information from book class and build line for file
                        lines.append(temp) #add generated line to line list
                    try: #error handling for write
                        bookfile.writelines(lines) #write line to bookfile
                        break#end loop
                    except (IOError, OSError): #catch IOErrors
                        print("\033[7mUnexpected IOError: attempt file access again?\033[0m") #notify operator of error
                        choice = input("(yes/no): ") #get choice from user
                        if choice == 'yes' or 'y':#check that user chose retry
                            continue #go back to start of loop
                        else:#user chose no
                            print("\033[7mUnable to save books.\033[0m") #notify user of failure
                            break#end loop
            except (FileNotFoundError, PermissionError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._book_path} to save books.\033[0m") #notify user of failure
                    break#end loop

    def save_authors(self, authors_dict):
        while True: #loop for error handling
            try: #error handling for file access
                with open(self._author_path,"w") as authorfile: #open authors.log as authorfile
                    lines = [] #empty line list
                    for key, author in authors_dict.items(): #iterate through authors dictionary
                        temp = f'{key}::{author.get_name()}::{author.get_biography()}\n' #generate line from author class information
                        lines.append(temp) #add generated line to lines list
                    try: #error handling for write
                        authorfile.writelines(lines) #write lines to authorfile
                        break#end loop
                    except (IOError, OSError): #catch IOErrors
                        print("\033[7mUnexpected IOError: attempt file access again?\033[0m") #notify operator of error
                        choice = input("(yes/no): ") #get choice from user
                        if choice == 'yes' or 'y':#check that user chose retry
                            continue #go back to start of loop
                        else:#user chose no
                            print("\033[7mUnable to save authors.\033[0m") #notify user of failure
                            break#end loop
            except (FileNotFoundError, PermissionError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._author_path} to save authors.\033[0m") #notify user of failure
                    break #end loop

    def save_users(self, users_dict):
        while True: #loop for error handling
            try: #error handling for file access
                with open(self._user_path,"w") as userfile: #open users.log as userfile
                    lines = [] #empty lines list
                    for key, user in users_dict.items(): #iterate through users dictionary
                        temp = f'{key}::{user.get_name()}::{user.get_library_id()}' #generate line from information in user class
                        if len(user.get_borrowed()) > 0: #check for borrowed books
                            for book in user.get_borrowed(): #iterate through list of borrowed books
                                temp = temp + f'::{book}' #add book to end of line
                            temp = temp + '\n' #end line with new line
                        else: #no borrorwed books
                            temp = temp + '::none\n' #end line with none and newline
                        lines.append(temp) #add line to lines list
                    try: #error handling for write
                        userfile.writelines(lines) #write lines to file
                        break#end loop
                    except (IOError, OSError): #catch IOErrors
                        print("\033[7mUnexpected IOError: attempt file access again?\033[0m") #notify operator of error
                        choice = input("(yes/no): ") #get choice from user
                        if choice == 'yes' or 'y': #check that user chose retry
                            continue #go back to start of loop
                        else: #user chose no
                            print("\033[7mUnable to save users.\033[0m") #notify user of failure
                            break#user chose no
            except (FileNotFoundError, PermissionError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._user_path} to save users.\033[0m") #notify user of failure
                    break#end loop

    def load_authors(self, authors_dict):
        while True: #loop for error handling
            try: #error handling for file access
                if not os.path.isfile(self._author_path): #check that doesn't exist authors.log file exist
                    with open(self._author_path, 'x') as authorfile: #create authors.log
                        authorfile.write("") #write to ensure file is created empty
                    break#end loop
                else: #authors.log exists
                    with open(self._author_path,'r') as author_file: #open authors.log as author_file
                        lines = author_file.readlines() #extract lines from file
                        for line in lines: #iterate through lines
                            buffer = line.split("::") #split lines along :: deliniators
                            if len(buffer) == 3: #ensure there are only as many entries as there should be
                                authors_dict[buffer[0]] = au.Author(buffer[1],buffer[2][:-1]) #use data from line to add an author to the authors dictionary
                    break#end loop
            except (FileNotFoundError, PermissionError, IOError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._author_path} to load authors.\033[0m") #notify user of failure
                    break#end loop

    def load_genres(self, genres_dict):
        while True: #loop for error handling
            try: #error handling for file access
                if not os.path.isfile(self._genre_path): #check that genres.log doesn't exist
                    with open(self._genre_path, 'x') as genrefile: #create genres.log as genrefile
                        genrefile.write("") #write to ensure file is created empty
                    break#end loop
                else: #genres.log exists
                    with open(self._genre_path,'r') as genres_file: #open genres.log as genrefile
                        lines = genres_file.readlines() #extract lines from file
                        for line in lines: #iterate through lines
                            buffer = line.split('::') #split line along :: deliniator
                            if len(buffer) == 4: #ensure not extra or missing data
                                genres_dict[buffer[0]] = gu.Genre(buffer[1],buffer[2], buffer[3][:-1]) #use line data to create new genre in genres dictionary
                        break#end loop
            except (FileNotFoundError, PermissionError, IOError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._genre_path} to load genres.\033[0m") #notify user of failure
                    break#end loop

    def load_books(self, books_dict, genre_dict):
        while True: #loop for error handling
            try: #error handling for file access
                if not os.path.isfile(self._book_path): #check that books.log doesn't exist
                    with open(self._book_path, 'x') as bookfile: #open books.log as bookfile
                        bookfile.write("") #write to ensure file created empty
                    break#end loop 
                else: #books.log exists
                    with open(self._book_path,'r') as books_file: #open books.log as books_file
                        lines = books_file.readlines() #extract lines from file
                        for line in lines: #iterate through lines
                            buffer = line.split('::') #split line using :: deliniator
                            if len(buffer) == 7: #check that there are only 7 data points in line
                                buffer[6] = buffer[6][:-1] #remove new line from final data point

                                t_year, t_month, t_day = buffer[4].split("/") #split date date into year, month, day
                                buffer[4] = dt.date(int(t_year), int(t_month), int(t_day)) #store date back as date object

                                if buffer[5] == 'Available': #check if book is available
                                    buffer[5] = True #store data as bool instead of string
                                elif buffer[5] == 'Borrowed': #check if book borrowed
                                    buffer[5] = False #store data as bool
        
                                description = genre_dict[buffer[6].lower()].get_description() #get description from genres dictionary for Book class initialization
                                category = genre_dict[buffer[6].lower()].get_category() #get category from genres dictionary for Book class initialization

                                books_dict[buffer[0]] = bu.Book(buffer[6], description, category, buffer[1], buffer[2], buffer[3], buffer[4], buffer[5]) #create new book in books dictionary using line data
                        break#end loop 
            except (FileNotFoundError, PermissionError, IOError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._book_path} to load books.\033[0m") #notify user of failure
                    break

    def load_users(self, user_dict):
        while True: #loop for error handling
            try: #error handling for file access
                if not os.path.isfile(self._user_path): #check that users.log doesn't exist
                    with open(self._user_path, 'x') as userfile: #create users.log as userfile
                        userfile.write("") #write to ensure file created empty
                    break#end loop
                else: #users.log exists
                    with open(self._user_path,"r") as userfile: #open users.log as userfile
                        lines = userfile.readlines() #extract lines
                        for line in lines: #iterate through lines
                            buffer = line.split('::') #split line using :: deliniator
                            buffer[len(buffer) - 1] = buffer[len(buffer) - 1][:-1] #remove new line from end of line
                            if len(buffer) == 4: #check if there are 4 data points in line
                                user_dict[buffer[0]] = uu.User(buffer[1],buffer[2]) #create user in user dictionary with no borrowed books
                            elif len(buffer) > 4:
                                borrowed = [] #list to store extracted borrowed books
                                for x in range(3,len(buffer)): #iterate through borrowed books only
                                    borrowed.append(buffer[x]) #add borrowed books to borrowed list
                                user_dict[buffer[0]] = uu.User(buffer[1],buffer[2]) #create user in user dictionary using line data
                                user_dict[buffer[0]].set_borrowed(borrowed) #add borrowed books to new user
                            else: # corrupted line
                                continue #go back to start of loop
                        break #end loop 
            except (FileNotFoundError, PermissionError, IOError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y':#check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._user_path} to load users.\033[0m") #notify user of failure
                    break#end loop
        

    def update_users(self, user_dict, key):
        while True: #loop for error handling
            try: #error handling for file access
                with open(self._user_path,'a') as user_file: #open users.log as user_file
                    temp = f'{key}::{user_dict[key].get_name()}::{user_dict[key].get_library_id()}\n' #build line from user class
                    try: #error handling for write
                        user_file.write(temp) #write new line to users.log
                        break#end loop
                    except (IOError, OSError): #catch IOErrors
                        print("\033[7mUnexpected IOError: attempt file access again?\033[0m") #notify operator of error
                        choice = input("(yes/no): ") #get choice from user
                        if choice == 'yes' or 'y':#check that user chose retry
                            continue #go back to start of loop
                        else:#user chose no
                            print("\033[7mUnable to update users.\033[0m") #notify user of failure
                            break#end loop
            except (FileNotFoundError, PermissionError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue#go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._user_path} to update users.\033[0m") #notify user of failure
                    break#end loop

    def update_authors(self, authors_dict, key):
        while True: #loop for error handling
            try: #error handling for file access
                with open(self._author_path, 'a') as author_file: #open authors.log as author_file
                    temp = f'{key}::{authors_dict[key].get_name()}::{authors_dict[key].get_biography()}\n' #generate line from author class
                    try: #error handling for write
                        author_file.write(temp) #append line to authors.log
                        break#end loop
                    except (IOError, OSError): #catch IOErrors
                        print("\033[7mUnexpected IOError: attempt file access again?\033[0m") #notify operator of error
                        choice = input("(yes/no): ") #get choice from user
                        if choice == 'yes' or 'y': #check that user chose retry
                            continue #go back to start of loop
                        else:#user chose no
                            print("\033[7mUnable to update authors.\033[0m") #notify user of failure
                            break #end loop
            except (FileNotFoundError, PermissionError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else:#user chose no
                    print(f"\033[7mUnable to open {self._author_path} to update authors.\033[0m") #notify user of failure
                    break #end loop

    def update_genres(self, genres_dict, key):
        while True: #loop for error handling
            try: #error handling for file access
                with open(self._genre_path, 'a') as genre_file: #open genres.log as genre_file
                    temp = f'{key}::{genres_dict[key].get_name()}::{genres_dict[key].get_description()}::{genres_dict[key].get_category()}\n' #generate line from genre class
                    try: #error handling for write
                        genre_file.write(temp) #append line to genres.log
                        break # end loop
                    except (IOError, OSError): #catch IOErrors
                        print("\033[7mUnexpected IOError: attempt file access again?\033[0m") #notify operator of error
                        choice = input("(yes/no): ") #get choice from user
                        if choice == 'yes' or 'y': #check that user chose retry
                            continue #go back to start of loop
                        else: #user chose no
                            print("\033[7mUnable to update genres.\033[0m") #notify user of failure
                            break #end loop
            except (FileNotFoundError, PermissionError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else: #user chose no
                    print(f"\033[7mUnable to open {self._genre_path} to update genres.\033[0m") #notify user of failure
                    break#end loop

    def update_books(self, books_dict, key):
        while True: #loop for error handling
            try: #error handling for file access
                with open(self._book_path, 'a') as book_file: #open books.log as book_file
                    temp = f'{key}::{books_dict[key].get_title()}::{books_dict[key].get_author()}::{books_dict[key].get_isbn()}::{books_dict[key].get_publication_date().strftime("%Y/%m/%d")}::{books_dict[key].get_status()}::{books_dict[key].get_name()}\n' #generate line from Book class
                    try: #error handling for write
                        book_file.write(temp) #append line to books.log
                        break #end loop
                    except (IOError, OSError): #catch IOErrors
                        print("\033[7mUnexpected IOError: attempt file access again?\033[0m") #notify operator of error
                        choice = input("(yes/no): ") #get choice from user
                        if choice == 'yes' or 'y': #check that user chose retry
                            continue #go back to start of loop
                        else: #user chose no
                            print("\033[7mUnable to update books.\033[0m") #notify user of failure
                            break #end loop
            except (FileNotFoundError, PermissionError, OSError):
                print("\033[7mUnable to access file for writing: attempt accessing file again?\033[0m") #notify operator of error
                choice = input('(yes/no): ') #get choice from user
                if choice == 'yes' or 'y': #check that user chose retry
                    continue #go back to start of loop
                else: #user chose no
                    print(f"\033[7mUnable to open {self._book_path} to update books.\033[0m") #notify user of failure
                    break#end loop

    def reload_all(self, author_dict, book_dict, genre_dict, user_dict):
        author_dict.clear() #clear author dictionary
        book_dict.clear() #clear book dictionary
        genre_dict.clear() #clear genre dictionary
        user_dict.clear() #clear user dictionary

        self.load_authors(author_dict) #load authors from file
        self.load_genres(genre_dict) #load genres from file
        self.load_books(book_dict,genre_dict) #load books from file
        self.load_users(user_dict) #load users from file

    def save_all(self, author_dict, book_dict, genre_dict, user_dict): 
        self.save_authors(author_dict) #save authors to file
        self.save_books(book_dict) #save books to file
        self.save_genres(genre_dict) #save genres to file
        self.save_users(user_dict) #save users to file

    def load_all(self, author_dict, book_dict, genre_dict, user_dict):
        if os.path.isfile(self._author_path) and os.path.isfile(self._book_path) and os.path.isfile(self._genre_path) and os.path.isfile(self._user_path): #Check that all files are found
            self.load_authors(author_dict) #load authors
            self.load_genres(genre_dict) #load genres
            self.load_books(book_dict, genre_dict) #load books
            self.load_users(user_dict) #load users
        else: #not all found
            if not os.path.isfile(self._author_path) and not os.path.isfile(self._book_path) and not os.path.isfile(self._genre_path) and not os.path.isfile(self._user_path): #check all missing
                self.load_authors(author_dict) #load authors to create authors.log
                self.load_genres(genre_dict) #load genres to create genres.log
                self.load_books(book_dict, genre_dict) #load books to create books.log
                self.load_users(user_dict) #load users to create users.log
            else:
                print("\033[7mUnable to locate all data files: Cancelling loading of save files. Please close program and restore files if you want to use Library Mangagement System with previously input information\033[0m") #notify user of failure to find all files
                while True: #loop in case of valid input
                    choice = input("Options for continuing:\n1. Delete all save files and start from empty state\n2.Quit Library Management System and investigate/restore save files\n Please enter your choice: ") #ask user how they want to proceed

                    if choice == '1': #chose to delete and start empty
                        if os.path.exists(self._author_path): #check if file is there
                            os.remove(self._author_path) #delete file
                        if os.path.exists(self._book_path): #check if file is there
                            os.remove(self._book_path) #delete file
                        if os.path.exists(self._genre_path): #check if file is there
                            os.remove(self._genre_path) #delete file
                        if os.path.exists(self._user_path): #check if file is there
                            os.remove(self._user_path) #delete file
                        
                        self.load_authors(author_dict) #load authors to create authors.log
                        self.load_genres(genre_dict) #load genres to create genres.log
                        self.load_books(book_dict, genre_dict) #load books to create books.log
                        self.load_users(user_dict) #load users to create users.log
                        break#end loop
                    elif choice == '2': #user chooses to close
                        sys.exit("Library Management System now closing for Investigation/Restoration of save files") #exit with goodbye message
                    else: #invalid choice
                        print("Invalid choice: Please try again") #notify of invalid input