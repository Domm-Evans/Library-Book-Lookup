#task 39

#program needs to options to:
#   add new books to db
#   update books in db
#   delete books from db
#   search the db

# The program should present the user with the following menu:
# 1. Enter book
# 2. Update book
# 3. Delete book
# 4. Search books
# 0. Exit



#import the modules
import pandas as pd
import sqlite3

#define function to create the table in the database using the predetermined list of books
def create_table(db, books):
    cursor.execute("""CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)""")
    cursor.executemany("""INSERT OR IGNORE INTO books(id, title, author, qty) VALUES(?,?,?,?)""", books)
    db.commit()

#Define home function that offer a list of options to use and directs to input choice.
def home():
    print("""\nMake a selection from below or exit:   
    Enter book (1)
    Update book (2)
    Delete book (3)
    Search book (4)
    View all books (5)
    Exit (0)\n""")
    selection = input("Input the code in the brackets for the selection you want: ")
    if selection == "1":
        add_book()
    elif selection == "2":
        update_book()
    elif selection == "3":
        delete_book()
    elif selection == "4":
        search_book()
    elif selection == "5":
        view_books()
    elif selection == "0":
        print("Goodbye")
        db.close()          #close the database when exit is selected 
    else:
        print("\nInvalid selection\n")
        home()


#define add book function
def add_book():
    while True:
        new_id, new_title, new_author, new_qty = input("What is the ID number? "),input("What is the book title? "), input("What is the Author's name? ") ,input("What is the quantity? ")
        #try converting inputs to int
        try:
            new_id = int(new_id)
            new_qty = int(new_qty)
            break                # Exit the while loop if both values are integers
        #if a non number is entered into id or qty then the function loops
        except ValueError:
            print("\nThis is not a number. Please enter a valid integer value for id and qty or '00' to return home.\n")    
    
    #now all data types are correct try inserting new book    
    try:
        cursor.execute("""INSERT INTO books(id,title,author,qty) VALUES(?,?,?,?)
        """,(new_id,new_title,new_author,new_qty))
        print("\nBook successfully added\n")
        db.commit()
    except Exception as e:      #if there is an error in inserting the new book this gets rolledback
        db.rollback()
        print("Invalid addition")
    home()


#update book function allows user to alter books in the db
def update_book():
    while True:
        book_id = input("What is the id of the book you would like to update? ")
        if book_id.isnumeric() == False:        #if the book_id input is not numeric repeat loop
            print("\nThis id is invalid.")
            continue
        elif book_id == "00":              #if the input is "00" return to home
            home()
        else:                                   
            book_id = int(book_id)                  #else if id is numeric and not 00 convert book id to int type
            update_column = input("What column would you like to update? ").lower()     #take the name of the column the update is needed in
            update = input("What would you like to change this to? ")                   #take the value that this should be changed to
            if update_column == "id" or update_column =="qty":                          #if the column needed for updating is id or qty
                try:                                
                    update = int(update)                                                #convert the update value to int and break the loop
                    break
                except ValueError:                                                      #if converting the update to value to int throws value error print error and repeat loop
                    print("\nThis is not a number. Please enter a valid integer value for id and qty.\n")
            else:                                                                       #if input is not for qty or id then break loop
                break
    
    try:             #update the chosen column indexed with the input id
        cursor.execute(f"""UPDATE books SET {update_column} = ? WHERE id = ? """, (update, book_id))
        cursor.execute(f"""SELECT * FROM books WHERE id = ?""",(book_id,))      #print the updated record
        search = cursor.fetchall()
        print(f"\n{search}")
        print("\nRecord updated.\n")
        db.commit()
    except Exception as e:              #any error causes a rollback to prevent damaging the db
        db.rollback
    home()

#function to delete records
def delete_book():
    deleted = input("Please give the ID of the book you would like to delete ")     #take input for book id
    cursor.execute("""SELECT count(*) FROM books WHERE id = ?""",(deleted,))        #count records with that id to check it exists
    count = cursor.fetchone()[0]
    if count== 0:                                                                   #if no records with that id exist tell user and return to homepage
        print("Record does not exist")
        home()
    else:
        cursor.execute("""DELETE FROM books WHERE id = ?""", (deleted,))            #if record exists then delete from db
        print("Record deleted")
    db.commit()
    home()

#function to search db for specific record
def search_book():
    while True:         #loop to check for errors
        column = input("What column do you want to search by (id, title, author or qty)? ").lower()      #take input for column that user wants to search in
        value = input("Input the value that you wish to search for. ")                                   #take input for value to search for

        if column == "id" or column =="qty":                                                             #if id or qty is requred try convert to integer
            try:
                value = int(value)
                break
            except ValueError:
                print("\nThis is not a number. Please enter a valid integer value for id and qty.\n")
        else:
            break
                
    cursor.execute(f"""SELECT * FROM books WHERE {column} = ?""",(value,))                               #search using given inputs and print
    search = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]                                                   #retrieve column names and convert to df for presentation
    df = pd.DataFrame(search, columns=columns)
    print(f"\n{df}")
    home()


#function to view all books in a neat display
def view_books():
    cursor.execute("""SELECT * FROM books ORDER BY id ASC""")           #select all books in order of id
    all_rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]                  #retrieve column names
    df = pd.DataFrame(all_rows, columns=columns)                        #convert to df for presentation
    print(f"\n{df}")
    home()

#main body
#initialise the variables
db = sqlite3.connect("ebookstore")
cursor = db.cursor()
print("connected" )

#List predetermined books to form initial db
books = [(3001, "A Tale of Two Cities", "Charles Dickens", 30), (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
         ( 3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25), (3004, "The Lord of the Rings", "J.R.R Tolkien", 37), 
         (3005, "Alice in Wonderland","Lewis Carroll", 12)]

#call to create predetermined table
create_table(db,books)

#run homepage function
home()

