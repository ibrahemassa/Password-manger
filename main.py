from tkinter import *
from tkinter import messagebox
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
import random

characters = {
    "letters" : ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
    "numbers" : ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    "symbols" : ['!', '#', '$', '%', '&', '(', ')', '*', '+']
}

def gen_password():
    password_list = [random.choice(characters["letters"]) for _ in range (random.randint(8, 10))]
    password_list += [random.choice(characters["symbols"]) for _ in range (random.randint(2, 4))]
    password_list += [random.choice(characters["numbers"]) for _ in range (random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)
    
    password_input.delete(0, END)
    password_input.insert(0, password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website:{
            "email": email,
            "password": password,
        }
    }

    if website == "" or email == "" or password == "":
        messagebox.showerror(title= "Error", message= "Please don't leave any field empty")
    else:
        ok = messagebox.askokcancel(title= website, message=f"You entered:\n Email: {email}\n Password: {password}\n Do you want to save?")
        if ok:
            try:
                with open("Data.json", mode= "r") as file:
                    data = json.load(file)
            
            except FileNotFoundError:
                with open("Data.json", mode= "w") as file:
                    json.dump(new_data, file, indent= 4)
            
            else:
                data.update(new_data)

                with open("Data.json", mode= "w") as file:
                    json.dump(data, file, indent= 4)
                    website_input.delete(0, END)
                    password_input.delete(0, END)
                    # email_input.delete(0, END)

            finally:
                window.clipboard_clear()
                window.clipboard_append(password)
# ----------------------------- Search -------------------------------- #
def search():
    website = website_input.get()
    try:
        with open("Data.json") as file:
            data = json.load(file)
    
    except FileNotFoundError:
        messagebox.showerror(title= "Error", message= "File not found!")
    
    except KeyError:
        messagebox.showerror(title= "Error", message= "Data not found!")
    
    else:
        email = data[website]['email']
        password = data[website]['password']
        messagebox.showinfo(title = f"Result for {website}", message= f"Email: {email}\nPassword: {password}")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx = 40, pady = 40)

canvas = Canvas(width= 200, height= 200)
img = PhotoImage(file = "logo.png")
canvas.create_image(100, 100, image = img)
canvas.grid(column= 1, row = 0)

#Labels:
website_label = Label(text = "Website:", font= ("Ariel",16,))
website_label.grid(column= 0, row= 1)

email_label = Label(text = "Email/Username:", font= ("Ariel",16,))
email_label.grid(column= 0, row= 2)

password_label = Label(text = "Password:", font= ("Ariel",16,))
password_label.grid(column= 0, row= 3)

#Inputs:
website_input = Entry(width= 21, font= ("Ariel",16,))
website_input.grid(column=1, row=1 , columnspan=1)
website_input.focus()

email_input = Entry(width= 35, font= ("Ariel",16,))
email_input.grid(column=1, row=2 , columnspan=2)

password_input = Entry(width= 21, font= ("Ariel",16,))
password_input.grid(column=1, row=3)

#Buttons:
generate_button = Button(text= "Generate Password", font= ("Ariel",12,), command= gen_password)
generate_button.grid(column=2, row= 3)

add_button = Button(text= "Add", width= 45, font= ("Ariel",12,), command= save)
add_button.grid(column= 1, row= 4, columnspan= 2)

search_button = Button(text= "Search", font= ("Ariel",12,), width=16, command= search)
search_button.grid(column= 2, row = 1)

window.mainloop()