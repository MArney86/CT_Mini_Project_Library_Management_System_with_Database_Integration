# CT_Mini_Project_Library_Management_System

Library Management System Mini Project for Coding Temple Software Engineering Course

## Table of Contents

1. Installing and Running the Application
    1. Installation
    2. Running the Application on Windows
    3. Running the Application on POSIX Operating Systems(Linux/Unix/BSD/MacOS)
    4. Setting Up the Database for Program Function
2. How to use the Library Management System
    1. Book Operations
    2. User Operations
    3. Author Operations
    4. Genre Operations
    5. Quit
3. Book Operations
    1. Add a new book
    2. Borrow a book
    3. Return a book
    4. Search for a book
    5. Display all books
    6. Return to previous menu
4. User Operations
    1. Add a new user
    2. View user details
    3. Display all users
    4. Return to previous menu
5. Author Operations
    1. Add a new author
    2. View author details
    3. Display all authors
    4. Return to previous menu
6. Genre Operations
    1. Add a new genre
    2. View genre details
    3. Display all genres
    4. Return to previous menu

## 1. Installing and Running the Application

### 1.1 Installation

Clone or download the repository to a directory.

### 1.2 Running the Application on Windows

    python .\Library_Management_System.py (if Python is setup in your system's PATH)
    [installation Directory]\python.exe .\Library_Management_System.py (no system PATH set)

### 1.3 Running the Application on POSIX Operating Systems(Linux/Unix/BSD/MacOS)

    python ./Contact_Management_System.py (if proper environment variables setup)
    python3 ./Contact_Management_System.py (some systems may require python3 command instead of python command)
    [install path]/python ./Contact_Management_System.py (no environment variable set)
    [install path]/python3 ./Contact_Management_System.py (alternative for some systems with no environment variable set)

### 1.4 Setting Up the Database for Program Function

please use the included `create database.sql` to create the required database if it does not already exist on your systems
update the variable in the connect database function within `connect_mysql.py` for your particular MySQL server

## 2. How to use the Library Management System

### 2.1 Book Operations

This selection will take you to the menu for handling book operations such as adding, borrowing, returning, or searching for and displaying books in the library.

### 2.2 User Operations

This selection will take you to the menu for handling user operations such as adding, displaying, or listing all the users in the library.

### 2.3 Author Operations

This selection will take you to the menu for handling Author operations such as adding, displaying information about, and listing all authors with records in the library system.

### 2.4 Genre Operations

This selection will take you to the menu for handling Genre operations such as adding, displaying information about, and listing all Genres recorded and available in the library system.

### 2.5 Quit

This selection will exit the program and return you to the system terminal/console.

## 3. Book Operations

### 3.1 Add a new book

This selection will ask you for title, author, ISBN, and publication date information, and prompt you to choose a genre for the book you want to add to the library system. If the genre for the book isn't in the menu, typing it in will prompt you to add it to the record of genres in the library system.

### 3.2 Borrow a book

This selection will ask you for the user and the book they want to borrow then record the book within the user information and set the the book as unavailable in it's information.

### 3.3 Return a book

This selection will ask you for the user and the book they want to return then remove the record of the book from the user information and set the book as available in it's information.

### 3.4 Search for a book

This selection will ask you if you want to search by title, author, ISBN, Genre, or if you want to return to the previous menu. Then it will search the input query for book in the library system that match that search and ask you to choose which one you want to display the information of.

### 3.5 Display all books

This selection prints out the information of all the books in the Library System.

### 3.6. Return to previous menu

This selection will return you to the previous menu.

## 4. User Operations

### 4.1 Add a new user

This selection will ask you for the new user's name, generate a Library ID for them and then add them to the Library user rolls with an empty Borrowed list.

### 4.2 View user details

This selection will ask you for the name or Library ID of the user whose information you wish to view (Name, Library ID, Borrowed titles list).

### 4.3 Display all users

This selection will print out the information of all the users in the Library System.

### 4.4 Return to previous menu

This selection will return you to the previous menu.

## 5. Author Operations

### 5.1 Add a new author

This selection will ask you for the name and a, preferably brief, biography of the author then add that information to the Library records.

### 5.2 View author details

This selection will ask you for the name of the author who you wish to view the information of then display it to you. You may be asked to choose from multiple choices if there are multiple authors with the same name.

### 5.3 Display all authors

This selection will print out the information of all the authors recorded in the Library System.

### 5.4 Return to previous menu

This selection will return you to the previous menu.

## 6. Genre Operations

### 6.1 Add a new genre

This selection will ask you for the name of the genre (i.e. Fantasy, Science Fiction, Biography...), a brief description of the genre, and then finally what category it falls under. Categories currently are Fiction, Non-fiction, Reference, and Periodicals.

### 6.2 View genre details

This selection will display details about the selected genre to the user.

### 6.3 Display all genres

This selection will print out the information of all the Genres recorded in the Library System.

### 6.4 Return to previous menu

This selection will return you to the previous menu.
