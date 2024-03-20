import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window = tk.Tk()
window.title("Library Management System")
window.geometry('600x500')
window.configure(bg = '#FFAC1C')

login_frame = tk.Frame(bg = '#FFAC1C')
system_frame = tk.Frame(bg = '#FFAC1C')


def create_table():
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('''CREATE TABLE IF NOT EXISTS Books (id TEXT PRIMARY KEY, title TEXT, isbn NUMERICAL, author TEXT, date TEXT, description TEXT, availability TEXT)''')
   conn.commit()
   conn.close()

def fetch_books():
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('SELECT * FROM Books')
   books = cursor.fetchall()
   conn.close()
   return books

def insert_books(id, title, isbn, author, date, description, availability):
   conn = sqlite3.connect('database.db')
   cursor =conn.cursor()
   cursor.execute('INSERT INTO Books (id, title, isbn, author, date, description, availability) VALUES (?,?,?,?,?,?,?)', 
                  (id, title, isbn, author, date, description, availability))
   conn.commit()
   conn.close()

def delete_books(id):
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('DELETE FROM Books WHERE id = ?', (id,))
   conn.commit()
   conn.close()

def update_books(id, new_title, new_isbn, new_author, new_date, new_description, new_availability):
   conn =sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('UPDATE Books SET title = ?, isbn = ?, author = ?, description = ?, availability = ? WHERE id = ?', 
                  (new_title, new_isbn, new_author, new_date, new_description, new_availability, id))

   conn.commit()
   conn.close()

def id_exists(id):
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('SELECT COUNT(*) FROM Books WHERE id = ?', (id,))
   result = cursor.fetchone()
   conn.close()
   return result[0] > 0


def create_login():
    def login():
        username="Admin"
        password="LibraryManagementSystem"
        if username_entry.get() == username and password_entry.get() == password:
            messagebox.showinfo(title="Success", message="Successful Login")
            login_frame.pack_forget()
        else:
            messagebox.showerror(title="Error", message="Incorrect username or password")
    login_label = tk.Label(login_frame, text = "Login", bg = '#FFAC1C', font=("Helvetica", 24))
    username_label = tk.Label(login_frame, text = "Username", bg = '#FFAC1C', font=("Helvetica"))
    password_label = tk.Label(login_frame, text = "Password", bg = '#FFAC1C', font=("Helvetica"))
    username_entry = tk.Entry(login_frame, font=("Helvetica", 15))
    password_entry = tk.Entry(login_frame, show = "*", font=("Helvetica", 15))
    login_button = tk.Button(login_frame, text = "Login", bg = '#FFFFFF', font=("Helvetica"), command = login)

    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    login_frame.pack()


def create_system():
 



 system_frame.pack()


create_table()
create_login()
create_system()
window.mainloop()


