from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import csv
import sqlite3

app = Flask(__name__)

def get_db_data():
    # Connect to SQLite database
    conn = sqlite3.connect('database.db')
    
    # Set row factory to sqlite3.Row to access by column names
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Query the database (example: selecting all data from a table called 'books')
    cursor.execute("SELECT * FROM book")
    
    # Fetch all data from the query
    data = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return data
    

@app.route('/')
def index():
    # Get data from the database
    data = get_db_data()
    
    # Pass data to the HTML template
    return render_template('index.html', data=data,type=type)

@app.route('/search', methods=['GET'])
def get_book_by_id():
    # Get the search term from the URL query parameter
    book_title = request.args.get('search')

    if not book_title:
        return render_template('index.html', data=None)

    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Execute the query using LIKE to search by title or author
    query = "SELECT * FROM book WHERE BookTitle LIKE ?"
    cursor.execute(query, ('%' + book_title + '%',))
    
    # Fetch the first result (or None if no result)
    book = cursor.fetchall()
    
    # Close the database connection
    conn.close()

    # Return the result to the template
    return render_template('index.html', data=book)

@app.route('/add_book_form')
def add_book_form():
    return render_template('add_book.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_title = request.form.get('BookTitle')
        author = request.form.get('BookAuthor')
        publisher = request.form.get('Publisher')
        year = request.form.get('YearOfPublication')
        isbn=request.form.get('ISBN')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO book (ISBN, BookTitle,BookAuthor,YearOfPublication,Publisher)
            VALUES (?,?,?,?,?)
        ''', (isbn, book_title, author, year, publisher))
        print(isbn, book_title,author,publisher,year)
        conn.commit()
        conn.close()

        return redirect(url_for('index'))  # Redirect back to the index page after adding the book
    
    return render_template('add_book.html')


@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    print(book_id)
    if request.method == 'POST':
        book_title = request.form['Book_Title']
        author = request.form['Author']
        publisher = request.form['Publisher']
        year = request.form['Year']
        

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE book 
            SET BookTitle = ?, BookAuthor = ?, Publisher = ?, YearOfPublication = ?
            WHERE ISBN = ?
        ''', (book_title, author, publisher, year, book_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))  # Redirect back to the index page after updating the book

    # If GET request, get book details for the modal
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()

    return render_template('index.html', book=book)

@app.route('/delete_book/<string:book_id>', methods=['POST'])
def delete_book(book_id):
    print("one\n")
    try:
        # Connect to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Execute the deletion query
        cursor.execute('DELETE FROM book WHERE ISBN = ?', (book_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        conn.close()

    # Redirect to the index page after deletion
    return redirect(url_for('index'))




if __name__=='__main__':
    app.run(debug=True)