# CT_Mini_Project_Library_Management_System
Library Management System Mini Project for Coding Temple Software Engineering Course

Table of Contents:
	1. Installing and Running the Application
	2. How to use the Library Management System
		a. Book Operations
    		b. User Operations
   		c. Author Operations
    		d. Genre Operations
    		e. Quit
	3. Book Operations
		a. Add a new book
        	b. Borrow a book
        	c. Return a book
        	d. Search for a book
        	e. Display all books
		f. Return to previous menu
	4. User Operations
		a. Add a new user
        	b. View user details
        	c. Display all users
		d. Return to previous menu
	5. Author Operations
		a. Add a new author
        	b. View author details
        	c. Display all authors
		d. Return to previous menu
	6. Genre Operations
        	a. Add a new genre
        	b. View genre details
        	c. Display all genres
		d. Return to previous menu
	7. Notes about automated save/load system

1. Installing and Running the Application:
	Installation: Clone or download the repository to a directory.

	Running the Application on Windows:
		python .\Contact_Management_System.py (if Python is setup in your system's PATH)
		[installation Directory]\python.exe .\Contact_Management_System.py (no system PATH set)

	Running the Application on POSIX Operating Systems(Linux/Unix/BSD/MacOS):
		python ./Contact_Management_System.py (if proper environment variables setup)
		python3 ./Contact_Management_System.py (some systems may require python3 command instead of python command)
		[install path]/python ./Contact_Management_System.py (no environment variable set)
		[install path]/python3 ./Contact_Management_System.py (alternative for some systems with no environment variable set)

2. How to use the Library Management System
		a. Book Operations
			This selection will take you to the menu for handling book operations such as adding, borrowing, returning, or searching for and displaying books in the library.
    		b. User Operations
			This selection will take you to the menu for handling user operations such as adding, displaying, or listing all the users in the library.
   		c. Author Operations
			This selection will take you to the menu for handling Author operations such as adding, displaying information about, and listing all authors with records in the library system.
    		d. Genre Operations
			This selection will take you to the menu for handling Genre operations such as adding, displaying information about, and listing all Genres recorded and available in the library system.
    		e. Quit
			This selection will exit the program and return you to the system terminal/console.
	3. Book Operations
		a. Add a new book
			This selection will ask you for title, author, ISBN, and publication date information, and prompt you to choose a genre for the book you want to add to the library system. If the genre for the book isn't in the menu, typing it in will prompt you to add it to the record of genres in the library system 
        	b. Borrow a book
			This selection will ask you for the user and the book they want to borrow then record the book within the user information and set the the book as unavailable in it's information.
        	c. Return a book
			This selection will ask you for the user and the book they want to return then remove the record of the book from the user information and set the book as available in it's information.
        	d. Search for a book
			This selection will ask you if you want to search by title, author, ISBN, Genre, or if you want to return to the previous menu. Then it will search the input query for book in the library system that match that search and ask you to choose which one you want to display the information of.
        	e. Display all books
			This selection prints out the information of all the books in the Library System.
		f. Return to previous menu
			This selection will return you to the previous menu.
	4. User Operations
		a. Add a new user
			This selection will ask you for the new user's name, generate a Library ID for them and then add them to the Library user rolls with an empty Borrowed list.
        	b. View user details
			This selection will ask you for the name or Library ID of the user whose information you wish to view (Name, Library ID, Borrowed titles list).
        	c. Display all users
			This selection will print out the information of all the users in the Library System.
		d. Return to previous menu
			This selection will return you to the previous menu.
	5. Author Operations
		a. Add a new author
			This selection will ask you for the name and a, preferably brief, biography of the author then add that information to the Library records.
        	b. View author details
			This selection will ask you for the name of the author who you wish to view the information of then display it to you. You may be asked to choose from multiple choices if there are multiple authors with the same name.
        	c. Display all authors
			This selection will print out the information of all the authors recorded in the Library System.
		d. Return to previous menu
			This selection will return you to the previous menu.
	6. Genre Operations
        	a. Add a new genre
			This selection will ask you for the name of the genre (i.e. Fantasy, Science Fiction, Biography...), a brief description of the genre, and then finally what category it falls under. Categories currently are Fiction, Non-fiction, Reference, and Periodicals.
        	b. View genre details
			This selection will ask you about 
        	c. Display all genres
			This selection will print out the information of all the Genres recorded in the Library System.
		d. Return to previous menu
			This selection will return you to the previous menu.
	7. Notes about automated save/load system
		The Library Management System automatically loads at startup previously saved information if all the appropriate save files are present. If the all the save files (authors.log, books.log, genres.log, and users.log), they will be created in an empty state. If one or more but not all save files are missing at startup, the user will be asked if they want to erase all existing files and start from an empty state or quit so that they can investigate and hopefully restore the missing files.
		#ADVANCED FILE FUNCTIONS: For advanced users only, please use with caution#
		From the Main Menu, the operator can input "Force Reload" and all information currently in loaded in memory will be cleared and information reloaded from the save files.
		From the Main Menu, the operator can input "Force Save" and all information currently in memory will be saved to the save files.