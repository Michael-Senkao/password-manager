from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
import json
import pyperclip
import random
from characters import characters

# ---------------------------- USER EMAIL ------------------------------- #
EMAIL = ""
DEFAULT_EMAIL = "example_email@gmail.com"

# ---------------------------- SEARCH FOR WEBSITE ------------------------------- #


def find_password():
    key = website_input.get().strip()
    if not key:
        messagebox.showwarning(
            'Warning', message='Please enter the website name')
        return

    try:
        with open('passwords.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror('Error', message='No Data File Found')
        return
    except JSONDecodeError:
        messagebox.showerror('Error', message='Data file is corrupted')
        return

    website = data.get(key.capitalize())
    if website:
        messagebox.showinfo(key, message=f"Email: {website['email']}\nPassword: {website['password']}")
    else:
        messagebox.showerror('Error', message='Website not in database')

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password(length):
    """Generate a random password of a given length with at least one number, one letter, and one symbol."""
    numbers = letters = symbols = 1  # At least one number, letter, and symbol

    letters += random.randint(0, length - 3)
    symbols += random.randint(0, length - letters - 2)
    numbers += length - letters - symbols - 1

    password_chars = (
        [random.choice(characters['numbers']) for _ in range(numbers)] +
        [random.choice(characters['symbols']) for _ in range(symbols)] +
        [random.choice(characters['letters']) for _ in range(letters)]
    )

    random.shuffle(password_chars)
    return "".join(password_chars)


def generate():
    """Generate a password, display it in the entry, and copy it to the clipboard."""
    length = random.randint(8, 20)
    password = generate_password(length)
    password_input.delete(0, END)
    password_input.insert(END, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def get_inputs():
    website = website_input.get().strip()
    email = username_input.get().strip()
    password = password_input.get().strip()

    if not (website and email and password):
        messagebox.showwarning(
            title="Warning", message="Please do not leave any field empty!")
        return

    is_ok = messagebox.askokcancel(
        title=website,
        message=f'Confirm details to continue\n\nwebsite: {website}\nemail: {email}\npassword: {password}'
    )
    if not is_ok:
        return

    new_data = {
        website.capitalize(): {
            'email': email,
            'password': password
        }
    }

    try:
        with open("passwords.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, JSONDecodeError):
        data = new_data
    else:
        data.update(new_data)

    with open('passwords.json', 'w') as data_file:
        json.dump(data, data_file, indent=4)

    website_input.delete(0, END)
    password_input.delete(0, END)
    website_input.focus()
    messagebox.showinfo(message="Password saved successfully!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

img = PhotoImage(file="./logo.png")
f1 = Frame()
f1.grid(row=0, column=0, columnspan=3)
canvas = Canvas(f1, width=200, height=200)
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

# FRAMES
password_frame = Frame()

website_frame = Frame()

# LABELS
website_label = Label(text="Website: ", font=("Arial", 10))
website_label.grid(row=1, column=0)
website_frame.grid(row=1, column=1, columnspan=3, sticky='w')
Label(text="", font=('Times New Roman', 2)).grid(row=2, column=0, columnspan=3)

username_label = Label(text="Email/Username: ", font=("Arial", 10))
username_label.grid(row=3, column=0)
Label(text="", font=('Times New Roman', 2)).grid(row=4, column=0, columnspan=3)

password_label = Label(text="Password: ", font=("Arial", 10))
password_label.grid(row=5, column=0)
password_frame.grid(row=5, column=1, columnspan=3, sticky='w')
Label(text="", font=('Times New Roman', 2)).grid(row=6, column=0, columnspan=3)

# ENTRIES
website_input = Entry(website_frame, width=22)
website_input.focus()
website_input.pack(side='left')
Label(website_frame, text="", font=('Times New Roman', 5)).pack(side="left")

username_input = Entry(width=41)
username_input.insert(0, EMAIL or DEFAULT_EMAIL)
username_input.grid(row=3, column=1, columnspan=2, sticky='w')

password_input = Entry(password_frame, width=22)
password_input.pack(side='left')
Label(password_frame, text="", font=('Times New Roman', 5)).pack(side="left")

# BUTTONS
generate_btn = Button(password_frame, text="Generate Password", bd=0.5, command=generate)
generate_btn.pack(side="left")

search_btn = Button(website_frame, text="Search", width=14, bd=0.5, command=find_password)
search_btn.pack(side="right")

add_btn = Button(text="Add", width=35, bd=0.5, command=get_inputs)
add_btn.grid(row=7, column=1, columnspan=2, sticky='w')

window.mainloop()
