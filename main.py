import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

window = tk.Tk()
window.title("Login Form")
window.geometry('500x450')
window.configure(bg = '#FFAC1C')


def open():
    new_slide="New Slide"



def login():
    username="Admin"
    password="LibraryManagementSystem"
    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title="Success", message="Successful Login")

    else:
        messagebox.showerror(title="Error", message="Incorrect username or password")
    


frame = tk.Frame(bg = '#FFAC1C')

login_label = tk.Label(frame, text = "Login", bg = '#FFAC1C', font=("Helvetica", 24))
username_label = tk.Label(frame, text = "Username", bg = '#FFAC1C', font=("Helvetica"))
password_label = tk.Label(frame, text = "Password", bg = '#FFAC1C', font=("Helvetica"))
username_entry = tk.Entry(frame, font=("Helvetica", 15))
password_entry = tk.Entry(frame, show = "*", font=("Helvetica", 15))
login_button = tk.Button(frame, text = "Login", bg = '#FFFFFF', font=("Helvetica"), command=login)

login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

frame.pack()

window.mainloop()


