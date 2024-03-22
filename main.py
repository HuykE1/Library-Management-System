import sqlite3          #importing each module required for the code
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window = tk.Tk()        #creating the window for the GUI to display
window.title("Library Management System")
window.geometry('800x650')
window.configure(bg = '#FFAC1C')

login_frame = tk.Frame(bg = '#FFAC1C')       #creating frames for each different system (login and library systems)
system_frame = tk.Frame(bg = '#FFAC1C')


def create_table():        #creates the database table using SQLite
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('''CREATE TABLE IF NOT EXISTS Books (id TEXT PRIMARY KEY, title TEXT, isbn NUMERICAL, author TEXT, date TEXT, description TEXT, availability TEXT)''')
   conn.commit()
   conn.close()

def fetch_books():         #function allowing the program to access the data from the database
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('SELECT * FROM Books')
   books = cursor.fetchall()
   conn.close()
   return books

def insert_books(id, title, isbn, author, date, description, availability):         #funtion to add the books into the database
   conn = sqlite3.connect('database.db')
   cursor =conn.cursor()
   cursor.execute('INSERT INTO Books (id, title, isbn, author, date, description, availability) VALUES (?,?,?,?,?,?,?)', 
                  (id, title, isbn, author, date, description, availability))
   conn.commit()
   conn.close()

def delete_books(id):         #funtion to delete the books from the database
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('DELETE FROM Books WHERE id = ?', (id,))
   conn.commit()
   conn.close()

def update_books(id, new_title, new_isbn, new_author, new_date, new_description, new_availability):         #functionto update the book in the database
   conn =sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('UPDATE Books SET title = ?, isbn = ?, author = ?, date = ?, description = ?, availability = ? WHERE id = ?', 
                  (new_title, new_isbn, new_author, new_date, new_description, new_availability, id))

   conn.commit()
   conn.close()

def id_exists(id):         #function to see if the id was previously used
   conn = sqlite3.connect('database.db')
   cursor = conn.cursor()
   cursor.execute('SELECT COUNT(*) FROM Books WHERE id = ?', (id,))
   result = cursor.fetchone()
   conn.close()
   return result[0] > 0


def create_login():        #creating the login window and adding its widgets and functions
    def login():        #creating the username and password for the admin to access the library system
        username="Admin"
        password="admin"
        if username_entry.get() == username and password_entry.get() == password:
            messagebox.showinfo(title="Success", message="Successful Login")
            login_frame.pack_forget()
            create_system()
        else:
            messagebox.showerror(title="Error", message="Incorrect username or password")
    login_label = tk.Label(login_frame, text = "Login", bg = '#FFAC1C', font=("Helvetica", 24))          #creating each widget and styling them for the login system
    username_label = tk.Label(login_frame, text = "Username", bg = '#FFAC1C', font=("Helvetica"))
    password_label = tk.Label(login_frame, text = "Password", bg = '#FFAC1C', font=("Helvetica"))
    username_entry = tk.Entry(login_frame, font=("Helvetica", 15))
    password_entry = tk.Entry(login_frame, show = "*", font=("Helvetica", 15))
    login_button = tk.Button(login_frame, text = "Login", bg = '#FFFFFF', font=("Helvetica"), command = login)

    login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)         #placing each widget on the window in specified spaces on the grid
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1, pady=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=30)

    login_frame.pack()        #centering the frame in the window


def create_system():       #creating the library system window and adding its widgets and functions

   def add_to_treeview():        #function to add data to the treeview and preventing data to be added to the same row
      books = fetch_books()
      tree.delete(*tree.get_children())
      for books in books:
         tree.insert('', tk.END, values=books)

   def insert():        #function to add the inputted book into the database
      id = id_entry.get()
      title = title_entry.get()
      isbn = isbn_entry.get()
      author = author_entry.get()
      date = date_entry.get()
      description = description_entry.get()
      availability = availability_options.get()
      if not (id and title and isbn and author and date and description and availability):
         messagebox.showerror('Error', 'Enter all fields')
      elif id_exists(id):
         messagebox.showerror('Error', 'ID already exists')
      else:
         insert_books(id, title, isbn, author, date, description, availability)
         add_to_treeview()
         clear()
         messagebox.showinfo('Success', 'Data has been added')

   def clear(*clicked):       #function to clear all entries of the entered data and unselecting the selected field on the treeview
      if clicked:
         tree.selection_remove(tree.focus())
         tree.focus('')
      id_entry.delete(0, tk.END)
      title_entry.delete(0, tk.END)
      isbn_entry.delete(0, tk.END)
      author_entry.delete(0, tk.END)
      date_entry.delete(0, tk.END)
      description_entry.delete(0, tk.END)
      availability_options.delete(0, tk.END)

   def display_data(event):         #function that displays the data of the selected field on the treeview in the entry boxes
      selected_item = tree.focus()
      if selected_item:
         row = tree.item(selected_item)['values']
         clear()
         id_entry.insert(0, row[0])
         title_entry.insert(0, row[1])
         isbn_entry.insert(0, row[2])
         author_entry.insert(0, row[3])
         date_entry.insert(0, row[4])
         description_entry.insert(0, row[5])
         availability_options.insert(0, row[6])
      else:
         pass



   def delete():        #function that deletes the selected field of the treeview
      selected_item = tree.focus()
      if not selected_item:
         messagebox.showerror('Error', 'Choose a book to delete')
      else:
         id = id_entry.get()
         delete_books(id)
         add_to_treeview()
         clear()
         messagebox.showinfo('Success', 'Data has been deleted')

   def update():        #function that updates the selected field of the treeview when an entry has been altered
      selected_item = tree.focus()
      if not selected_item:
         messagebox.showerror('Error', 'Choose a book to update')
      else:
         id = id_entry.get()
         title = title_entry.get()
         isbn = isbn_entry.get()
         author = author_entry.get()
         date = date_entry.get()
         description = description_entry.get()
         availability = availability_options.get()
         update_books(id, title, isbn, author, date, description, availability)
         add_to_treeview()
         clear()
         messagebox.showinfo('Success', 'Data has been updated')



   system_label = tk.Label(system_frame, text = "Library Management System", bg = '#FFAC1C', font = ("Helvetica", 24))        #creating the widgets for the library system frame including their style and functions
   id_label = tk.Label(system_frame, text = "Book ID", bg = '#FFAC1C', font = ("Helvetica")) 
   id_entry = tk.Entry(system_frame, font = ("Helvetica"))
   title_label = tk.Label(system_frame, text = "Book Title", bg = '#FFAC1C', font = ("Helvetica"))
   title_entry = tk.Entry(system_frame, font = ("Helvetica"))
   isbn_label = tk.Label(system_frame, text = "ISBN Number", bg = '#FFAC1C', font = ("Helvetica"))
   isbn_entry = tk.Entry(system_frame, font = ("Helvetica"))
   author_label = tk.Label(system_frame, text = "Author", bg = '#FFAC1C', font = ("Helvetica"))
   author_entry = tk.Entry(system_frame, font = ("Helvetica"))
   date_label = tk.Label(system_frame, text = "Date", bg = '#FFAC1C', font = ("Helvetica"))
   date_entry = tk.Entry(system_frame, font = ("Helvetica"))
   description_label = tk.Label(system_frame, text = "Description", bg = '#FFAC1C', font = ("Helvetica"))
   description_entry = tk.Entry(system_frame, font = ("Helvetica"))
   availability_label = tk.Label(system_frame, text = "Availability", bg = '#FFAC1C', font = ("Helvetica"))
   options = ['Available', 'Unavailable']
   availability_options = ttk.Combobox(system_frame, font = ("Helvetica"), values=options, state='readonly')
   availability_options.set('Available')
   add_button = tk.Button(system_frame, text = "Add Book", bg= '#FFFFFF', font= ("Helvetica", 15), command= insert)
   delete_button = tk.Button(system_frame, text = "Delete Book", bg = '#FFFFFF', font = ("Helvetica", 15), command=  delete)
   update_button = tk.Button(system_frame, text = "Update Book", bg = '#FFFFFF', font = ("Helvetica", 15), command= update)

   
   system_label.grid(row=0, column=2, columnspan=2, sticky="news", pady=40)         #placing the widgets in desired places on the frame using a grid
   id_label.grid(row=1, column=0)
   id_entry.grid(row=1, column=1)
   title_label.grid(row=2, column=0)
   title_entry.grid(row=2, column=1)
   isbn_label.grid(row=3, column=0)
   isbn_entry.grid(row=3, column=1)
   author_label.grid(row=4, column=0)
   author_entry.grid(row=4, column=1)
   date_label.grid(row=5, column=0)
   date_entry.grid(row=5, column=1)
   description_label.grid(row=6, column=0)
   description_entry.grid(row=6, column=1)
   availability_label.grid(row=7, column=0)
   availability_options.grid(row=7, column=1)
   delete_button.grid(row=8, column=0, pady=30)
   add_button.grid(row=8, column=1, pady=30)
   update_button.grid(row=8, column=2, pady=30)

   style = ttk.Style(system_frame)        #setting the style of the frame and treeview
   style.theme_use('classic')
   style.configure('TreeView', bg = '#FFFFFF', font = ("Helvetica"))
   style.map('TreeView', bg = [('selected', '#FFAC1C')])

   tree = ttk.Treeview(system_frame, height=15)

   tree['columns'] = ('ID', 'Title', 'ISBN', 'Author', 'Date', 'Description', 'Availability')

   tree.column('#0', width=0, stretch=tk.NO)          #removing the first column that is blank
   tree.column('ID', anchor=tk.CENTER, width=120)
   tree.column('Title', anchor=tk.CENTER, width=120)
   tree.column('ISBN', anchor=tk.CENTER, width=120)
   tree.column('Author', anchor=tk.CENTER, width=120)
   tree.column('Date', anchor=tk.CENTER, width=120)
   tree.column('Description', anchor=tk.CENTER, width=120)
   tree.column('Availability', anchor=tk.CENTER, width=120)

   tree.heading('ID', text='ID')       #setting the headings of each field
   tree.heading('Title', text='Title')
   tree.heading('ISBN', text='ISBN')
   tree.heading('Author', text='Author')
   tree.heading('Date', text='Date')
   tree.heading('Description', text='Description')
   tree.heading('Availability', text='Availability')

   tree.grid(row=2, column=3, rowspan=4)

   tree.bind('<ButtonRelease>', display_data)         #when a row is clicked, it will display the data
  
   add_to_treeview()       #calling the function to display the treeview

   system_frame.pack()        #centering the frame in the window
   
   



create_login()       #calling the funtion to display the login frame
window.mainloop()       #executes the window


