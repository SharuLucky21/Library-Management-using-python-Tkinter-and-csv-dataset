import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import date

# CSV file paths
books_file = 'books.csv'
issued_books_file = 'issued_books.csv'
users_file = 'users.csv'  # A simple CSV to store login credentials (username, password, role)

# Initialize CSV files if they don't exist
def init_csv_files():
    if not os.path.exists(books_file):
        with open(books_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Book ID', 'Title', 'Author', 'Status'])  # Column headers

    if not os.path.exists(issued_books_file):
        with open(issued_books_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Book ID', 'User', 'Issue Date'])

    if not os.path.exists(users_file):
        with open(users_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Password', 'Role'])  # Column headers
            # Add default users (you can change the passwords later)
            writer.writerow(['librarian', 'librarian123', 'Librarian'])
            writer.writerow(['student', 'student123', 'Student'])

# Login function to verify credentials and open the respective interface
def login():
    username = entry_username.get()
    password = entry_password.get()
    found = False

    with open(users_file, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == username and row[1] == password:
                found = True
                role = row[2]
                if role == 'Librarian':
                    open_librarian_interface()
                elif role == 'Student':
                    open_student_interface()
                break

    if not found:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# Function to add a new book to books.csv (Librarian only)
def add_book():
    book_id = entry_book_id.get()
    title = entry_title.get()
    author = entry_author.get()

    if book_id and title and author:
        with open(books_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([book_id, title, author, 'Available'])
        messagebox.showinfo("Success", "Book added successfully!")
        entry_book_id.delete(0, tk.END)
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

# Function to display all books in a new window
def view_books():
    new_window = tk.Toplevel()
    new_window.title("View Books")
    
    tree = ttk.Treeview(new_window, columns=("Book ID", "Title", "Author", "Status"), show='headings')
    tree.heading("Book ID", text="Book ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Status", text="Status")
    tree.pack(fill=tk.BOTH, expand=True)
    
    with open(books_file, newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            tree.insert("", tk.END, values=row)

# Function to issue a book to a user (Student)
def issue_book():
    book_id = entry_book_id.get()
    user_name = entry_user.get()

    if book_id and user_name:
        books = []
        found = False
        with open(books_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == book_id and row[3] == 'Available':
                    row[3] = 'Issued'
                    found = True
                books.append(row)

        if found:
            with open(books_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(books)
                
            with open(issued_books_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([book_id, user_name, str(date.today())])
            messagebox.showinfo("Success", "Book issued successfully!")
            entry_book_id.delete(0, tk.END)
            entry_user.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Book is not available or invalid ID!")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

# Function to return a book (Student)
def return_book():
    book_id = entry_book_id.get()

    if book_id:
        books = []
        found = False
        with open(books_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == book_id and row[3] == 'Issued':
                    row[3] = 'Available'
                    found = True
                books.append(row)

        if found:
            with open(books_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(books)
            messagebox.showinfo("Success", "Book returned successfully!")
            entry_book_id.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Invalid Book ID or Book not issued!")
    else:
        messagebox.showwarning("Input Error", "Please enter Book ID!")

# Function to delete a book (Librarian only)
def delete_book():
    book_id = entry_book_id.get()

    if book_id:
        books = []
        found = False
        with open(books_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == book_id:
                    found = True
                    continue
                books.append(row)

        if found:
            with open(books_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(books)
            messagebox.showinfo("Success", "Book deleted successfully!")
            entry_book_id.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "Invalid Book ID!")
    else:
        messagebox.showwarning("Input Error", "Please enter Book ID!")

# Function to open Librarian interface
def open_librarian_interface():
    root.withdraw()  # Hide the login window
    librarian_window = tk.Toplevel()
    librarian_window.title("Librarian Interface")

    # Librarian Controls
    tk.Label(librarian_window, text="Book ID").grid(row=0, column=0)
    global entry_book_id
    entry_book_id = tk.Entry(librarian_window)
    entry_book_id.grid(row=0, column=1)

    tk.Label(librarian_window, text="Title").grid(row=1, column=0)
    global entry_title
    entry_title = tk.Entry(librarian_window)
    entry_title.grid(row=1, column=1)

    tk.Label(librarian_window, text="Author").grid(row=2, column=0)
    global entry_author
    entry_author = tk.Entry(librarian_window)
    entry_author.grid(row=2, column=1)

    tk.Button(librarian_window, text="Add Book", command=add_book).grid(row=3, column=0)
    tk.Button(librarian_window, text="Delete Book", command=delete_book).grid(row=3, column=1)
    tk.Button(librarian_window, text="View Books", command=view_books).grid(row=4, column=0)
    tk.Button(librarian_window, text="Exit", command=librarian_window.destroy).grid(row=4, column=1)

# Function to open Student interface
def open_student_interface():
    root.withdraw()  # Hide the login window
    student_window = tk.Toplevel()
    student_window.title("Student Interface")

    tk.Label(student_window, text="Book ID").grid(row=0, column=0)
    global entry_book_id
    entry_book_id = tk.Entry(student_window)
    entry_book_id.grid(row=0, column=1)

    tk.Label(student_window, text="User").grid(row=1, column=0)
    global entry_user
    entry_user = tk.Entry(student_window)
    entry_user.grid(row=1, column=1)

    tk.Button(student_window, text="Issue Book", command=issue_book).grid(row=2, column=0)
    tk.Button(student_window, text="Return Book", command=return_book).grid(row=2, column=1)
    tk.Button(student_window, text="View Books", command=view_books).grid(row=3, column=0)
    tk.Button(student_window, text="Exit", command=student_window.destroy).grid(row=3, column=1)

# Main login window setup
root = tk.Tk()
root.title("Library Management System - Login")

# Username and Password fields
tk.Label(root, text="Username").grid(row=0, column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)

tk.Label(root, text="Password").grid(row=1, column=0)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1)

# Login Button
tk.Button(root, text="Login", command=login).grid(row=2, column=1)

# Initialize CSV files and start the application
init_csv_files()
root.mainloop()
