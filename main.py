import json
import tkinter
from tkinter.constants import DISABLED, END, INSERT
from tkinter.font import ITALIC
import requests
import json
import tkinter as tk
from tkinter import Entry, Image, Text, messagebox
from PIL import ImageTk, Image
import hashlib

global _id
_id = None

#window
root = tk.Tk()
root.config(background='#B4C6A6')
frame = tk.Frame(root)
frame.pack()
root.resizable(width=False, height=False)
root.title("iNote")
#window size
root.geometry('600x400')
root.wm_attributes('-transparent')
#background image
bg = ImageTk.PhotoImage(Image.open("images/bg.jpg"))
img1 = ImageTk.PhotoImage(Image.open("images/bg2.png"))
img2 = ImageTk.PhotoImage(Image.open("images/bg1.jpg"))
# Show image using label
label1 = tk.Label( root, image = bg)
label1.place(x = 0,y = 0)


#login entry
username_label = tk.Label(root, text="Username")
username_label.place(x=100, y=103)
username_entry = tk.Entry(root)
username_entry.place(x=200, y=100)
password_label = tk.Label(root, text="Password")
password_label.place(x=100, y=150)
Password_entry = tk.Entry(root, show="*")
Password_entry.place(x=200, y=150)



def destroy_widgets():
    for widegets in root.winfo_children():
        widegets.destroy()



def view_notes():
    destroy_widgets()
    tk.Label(root, image=img2).place(x=0, y=0)
    user_id = _id
    req_notes = requests.get(f'http://127.0.0.1:5000/note/{user_id}')
    notes_data = req_notes.text
    notes_data1 = json.loads(notes_data)
    notes_data3 = []
    data = ""
    try:
        for user in notes_data1['notes']:
            notes = user['notes']
            notes_data3.append(notes)

       
        for note in notes_data3:
            data = f"{note}\n" + data + "\n"  
              
        label1 = tk.Text(root, spacing2=5, background="#2E4C6D", height=5, font=("Times New Roman", 16), border=0, width=50, foreground='#F7F7F7')
        label1.insert(INSERT, f"{data}")
        label1.place(x=130, y=50)
        label1.config(state=DISABLED)
        root.update()
    except:
        tk.Label(root, text="You have no notes saved").place(x=200, y=150)
    back_button = tk.Button(root, text="Back", command=after_login)
    back_button.place(x=300, y=200)
    return data


def add_notes():
    destroy_widgets()
    bg3 = tk.Label(root, image=img2).place(x=0, y=0)

    tk.Label(root, text="Write a note").place(x=270, y=50)

    note_widget = tk.Text(root, width=50, height=10)
    note_widget.place(x=150, y=100)
    
    back_button = tk.Button(root, text="Back", command=after_login)
    back_button.place(x=350, y=280)
    
    def save_notes():
        note = note_widget.get("1.0",'end-1c')
        user_id = _id
        payload = {"note": note, "user_id": user_id}
        if len(note) > 1:
            req = requests.post('http://127.0.0.1:5000/note', data=payload)
            return messagebox.showinfo('successful', "Note added successfuly")

    save_button = tk.Button(root, text="Save", command=save_notes)
    save_button.place(x=450, y=280)

def after_login():
    bg3 = tk.Label(root, image=img2).place(x=0, y=0)
    add_notes_button = tk.Button(root, text="Add notes", width=50, command=add_notes)
    view_notes_button = tk.Button(root, text="View notes", width=50, command=view_notes)
    delete_notes_button = tk.Button(root, text="Delete notes", width=50)
    view_notes_button.place(x=50, y=100)
    add_notes_button.place(x=50, y=150)
    delete_notes_button.place(x=50, y=200)

def check_user(io=None):
    req = requests.get('http://127.0.0.1:5000/users')
    print(req.status_code)
    req = req.text
    req = json.loads(req)
    username = username_entry.get()
    password = Password_entry.get()
    password = hashlib.sha256(password.encode()).hexdigest()

    for usernames in req['users']:

        user_id = usernames['ID']
        user_password = usernames['password']
        usernames = usernames['username']
         
        if username == usernames:
            if password == user_password:
                messagebox.showinfo("Successful", "Login successful")
                global _id
                _id = user_id
                destroy_widgets()
                return after_login()
            print(user_id)
            return messagebox.showinfo("ERROR", "Invalid username or password")
    
    return messagebox.showinfo("ERROR", "Invalid username or password")



def register():
    register_window = tk.Toplevel(root)
    register_window.resizable(width=False, height=False)
    register_window.wm_attributes('-transparent')
    register_window.config(background="#E3D18A")
    frame = tk.Frame(register_window)
    frame.pack()
    register_window.title("Registration")
    register_window.geometry("600x400")
    logo1 = tk.Label(register_window, image=img1)
    logo1.pack()

    color = "#DA723C"
    color2 = "#E27802"
    description_label = tk.Label(register_window, text="Welcome to #1 Note writer application", font=('Times New Roman',20, 'italic'), background=color, foreground='#F0EBCC').place(x=120 , y=100)
    username_label2 = tk.Label(register_window, text="username", background=color2, foreground='#F0EBCC')
    username_label2.place(x=130, y=200)

    username_register = tk.Entry(register_window, background="#EAEAEA")
    username_register.place(x=220, y=200)

    password_label2 = tk.Label(register_window, text="password", background=color2, foreground='#F0EBCC')
    password_label2.place(x=130, y=240)

    password_register = tk.Entry(register_window, show="*", background="#EAEAEA")
    password_register.place(x=220, y=240)
    
    

    def check_register():
        username = username_register.get()
        password = password_register.get()

        username = username.lower()
        password = password.lower()

        req = requests.get('http://127.0.0.1:5000/users')
        req = req.text
        req = json.loads(req)
        users = req['users']
        for user in users:
            username1 = user['username']
            if username1 == username:
                return messagebox.showerror("ERROR", "User name already exists")


        if len(password) < 8:
            return messagebox.showinfo('ERROR', "password must be greater than 8 charachters")
    
        payload = {"username": f"{username}", "password": f"{password}"}
        post = requests.post('http://127.0.0.1:5000/register', data=payload)
        tk.Label(register_window, text="Registeration successful").place(x=270, y=320)
        messagebox.showinfo("Success", "User created successfuly")
        return register_window.destroy()
    
    register_button = tk.Button(register_window, text="Register", command=check_register)
    register_button.place(x=270, y=290)


#login button
login_button = tk.Button(root, text="Login", foreground='green', command=check_user)
login_button.place(x=260, y=200)

root.bind('<Return>', check_user)

#registeration button
register_button = tk.Button(root, text="Register", foreground="blue", command=register)
register_button.place(x=260, y=300)



root.mainloop()