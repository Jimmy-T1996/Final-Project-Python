'''
Author: Jimmy Torres
Program: Password Manager
Last Date Edited: 20250504

Program Details:
This program is a password manager built to incorporate the tkinter and cryptography library.

This program features:
-Password Generation
-Creating, saving, and deleting titles of entries to a CSV file.
-Deleting Entries.
-Decrypts and Encrypts CSV file using an AES/HMAC 256-bit symmetric key.
-The program acts as an interpreter for the key and the user does not need to manually decrypt/encrypt.

The program runs out of the root window and opens other functions in different window(new_window).
Most of the logic originated from the password Generator instruction and was translated to use
widgets in tkinter library. Certain functions such as the accounts viewer were added later
after basic functions were proven to work. 

Most of the resources used were from Youtube, W3schools.com, and forums pertaining to coding including
reddit.com, GeeksforGeeks.com, and Stack Overflow.  
All resources used will be included in technical documentation for this program.

Notes: 
-All functions working
-Encryption command fixed in root windows's "close" widget.
-CSV file can be written and saved. No error in encryption/decryption.
-Key is working.

Potential issues:

-titles can be repeated/ if one title is deleted, several of the same can be deleted at once.
-closing program can potentially corrupt file (from crashes and manually ending program).
-Opening CSV file while program is actively opening, closing, and editing information
can corrupt CSV file entirely.
-if key is edited in any way, a new key must be generated.
-code can be restructered/simplified for developer side.
'''

from tkinter import * #tkinter is imported. Widgets used in this program are from the tkinter library.
from PasswordGenerator import char_list1,char_list2 #Character lists in original PasswordGenerator file.
import random #Random used for randomly generated functions.
import csv #CSV creating and editing is done with this library.
import os # OS is imported for directory manipulation.
from cryptography.fernet import Fernet #Cryptography used for encrypt/decrypt functions.
root = Tk() #root is essentially the GUI windows. (does not run in python terminal)
root.title("Password Generator") #Title of GUI Window

root.configure(bg="#2e2e2e") #Background color of dark grey added to all windows
btn_bg = "#444" #Lighter grey buttons gives contrast.
btn_fg = "white" #White text to make it readable.
btn_active_bg = "#555" #When button is clicked on, different grey is shown. If deleted, button turns white.
default_font = ("Courier New", 12, "bold") # Font, text size, bold text

#This list will be used to store the individually generated characters of each password.
#This also gets cleared with every password iteration.
randlist = []
#Joined characters will create an output(password) and be saved here. 
new_password = []
#These lists serves as the content needed to write and save new .CSV files.
password_output = []
title = []
username = []
password = []

#Upon pressing the "Close" button/widget, the program will encrypt the file again befor closing.
#This is to ensure that the encryption function is called before closing the application.
#The current Configuration works with both the close button and 'X' on windows.
def disabled_close_button(root):
    #This function is structured to run with a protocol associated to closing the window of the program.
    #Before closing (.destroy) the encryption function is called. The program closes in this exact order.
    def on_closing():
        encrypt_file()
        root.destroy() 
    root.protocol("WM_DELETE_WINDOW", on_closing)
#the structured function is called.
disabled_close_button(root)

#When this function is called, a new window is opened with a different GUI.
def password_gen1():

    #New window is created and becomes the "top level" window. If this window is closed, program is still running (root window is open).
    new_window = Toplevel(root) #To ensure there is only one root, the new window is titled 'new_window' within the program.
    new_window.title("Password Generator") #Title on window bar which displays to the user.
    new_window.geometry("700x950") #Window size is manually set to accommodate size and layout of grid.
    new_window.configure(bg="#2e2e2e")#window background is a lighter gray.
    
    btn_bg = "#444" #Equivalent to a darker gray (button background)
    btn_fg = "white" #Text is white (foreground)
    default_font = ("Courier New", 12, "bold") #Text is black by default, the rest is developer prefence.

    #
    new_window.columnconfigure(0, weight=1)

    #Password generation buttons are displayed with these widgets. Their fonts/colors are the same attributes as the root window.
    #The 'Label' boxes are only boxes of text that cannot be changed.
    instruction_char = Label(new_window, text="How many Characters Do \nYou need In Your Password?", bg=btn_bg, fg=btn_fg, font=default_font)
    #Entry box ('input' in python terminal) supplements above instruction. This will get passed to the password generator function.
    user_input1 = Entry(new_window, width=35, border=8)

    #The next 2 lines repeat the same structure as above.
    instruction_passwords = Label(new_window, text="How Many Passwords Do \nYou Need?", bg=btn_bg, fg=btn_fg, font=default_font)
    user_input2 = Entry(new_window, width=35, border=8)

    #In Tkinter, calling functions requires that the 'command=' syntax call the function with the button it is associated with.
    #'lambda' is required for functions where arguments are passed. Without this, an error will occur. 
    generate_password = Button(new_window, text="Generate with special characters", bg=btn_bg, fg=btn_fg, font=default_font,
                                command=lambda: generate_1(user_input1.get(), user_input2.get()))
    generate_password2 = Button(new_window, text="Generate WITHOUT special characters", bg=btn_bg, fg=btn_fg, font=default_font,
                                 command=lambda: generate_2(user_input1.get(), user_input2.get()))
    #The 'close' button is uses the '.destroy' method to close the current window.
    close_btn = Button(new_window, text="Close", command=new_window.destroy, bg=btn_bg, fg=btn_fg, font=default_font)

    #The output box below is what the user will see when the passwords are generated. This box changes outputs
    # depending on the inputs.

    #The output variable will need to be a global variable to pass information between functions.
    global output
    output = Text(new_window, width=60, height=25, bg="gray", fg="black", font=("Courier New", 12, "bold"))

    #Output is set up to be centered in the window, with centered text.
    output.tag_configure("center", justify='center')
    #This is the default text in the text box. It will be deleted after the user attempts to generate passwords.
    output.insert("1.0", "Passwords Generated here")
    output.tag_add("center", "1.0", "end")
    #The box containing text cannot be edited (disabled).
    output.configure(state="disabled")

    #This section is the format of all the widgets in the window. Pady, and padx are the spacing values.
    #only one column is active (0) and 7 rows are used.
    instruction_char.grid(row=0, column=0, pady=10)
    user_input1.grid(row=1, column=0, pady=20, padx=10)

    instruction_passwords.grid(row=2, column=0, pady=10)
    user_input2.grid(row=3, column=0, pady=20, padx=10)

    generate_password.grid(row=4, column=0, pady=15)
    generate_password2.grid(row=5, column=0, pady=15)
    close_btn.grid(row=6, column=0, pady=15)

    output.grid(row=7, column=0, pady=20)
#This function is only information that briefly explains why password creation is important.
#The attributes are identical to the root window.
def sos():
    new_window = Toplevel(root)  
    new_window.title("Passwords Information")
    new_window.geometry("800x400")
    new_window.configure(bg="#2e2e2e")
    btn_bg = "#444"
    btn_fg = "white"
    btn_active_bg = "#555"
    default_font = ("Courier New", 12, "bold")

    #The columns 'weight' values reflect how they expand if their is available space. A value
    #of zero gives no expansion. A value of 2 doubles the size.
    new_window.columnconfigure(0, weight=1)
    new_window.columnconfigure(1, weight=0)
    new_window.columnconfigure(2, weight=1)
    #Paragraph has attributes at the end of the text. Similar to HTML, text wraps and is justified left of the box.
    password_info = Label(new_window,
                          text="    Password creation does not need to be complicated, but it " \
                          "does need to be well thought out. The Cybersecurity & Infrastructure" \
                          " Security Agency (CISA) recommends that a user has a password length " \
                          "of ATLEAST 16 characters.\n    This should include numbers, special characters, " \
                          "non-related phrases — if you plan to include phrases at all. When creating a " \
                          "long list of accounts with various passwords, you should be able to access " \
                          "them. CISA also reccomends you use a reputable password manager. Ensure that " \
                          "you do not re-use passwords for several accounts and that your passwords do not " \
                          "follow a naming convention, such as: 'Password2023' and '20Password23'.\n"
                          "    If Multifactor Authentication is offered by the services you are using, " \
                          "it is recommended to set up the service to mitigate any possible exploits." \
                          "CISA currently reports that 99% of user who implement MFA, do not get hacked.\n"
                          "    For more information on password creation, please visit:\n"
                          "https://www.cisa.gov/secure-our-world/use-strong-passwords",
                            bg=btn_bg, fg=btn_fg, font=default_font, wraplength=700, justify="left")
    #Layout of text box.
    password_info.grid(row=0, column=1)
    #User may close this window here.
    close_btn = Button(new_window, text="Close", command=new_window.destroy, bg=btn_bg, fg=btn_fg, font=default_font)
    close_btn.grid(row=1, column=1, pady=10)

#Password manager window opens a new window and has new options.
def password_manager():
    new_window = Toplevel(root)  
    new_window.title("Password Manager")
    new_window.configure(bg="#2e2e2e")
    btn_bg = "#444"
    btn_fg = "white"
    btn_active_bg = "#555"
    default_font = ("Courier New", 12, "bold")

    button_first = Button(new_window, text="Edit Account List", height=4, width=60,
                      bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, activeforeground=btn_fg, 
                      font=default_font, command=create_account) 
    button_second = Button(new_window, text="View Account List", height=4, width=60,
                      bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, activeforeground=btn_fg, 
                      font=default_font, command=view_accounts) 
    close_btn = Button(new_window, text="Close", command=new_window.destroy, bg=btn_bg, fg=btn_fg, font=default_font)

#Second button removed. The second button function was moved into button_first for simplicity.
    button_first.grid(row=1, column=0, columnspan=4, padx=12, pady=10)
    button_second.grid(row=2, column=0, columnspan=4, padx=12, pady=10)
    close_btn.grid(row=3, column=0, columnspan=4, padx=12, pady=10)
#Interface for the Create Account window.
def create_account():
    new_window = Toplevel(root)  
    new_window.title("Account List Creator")
    new_window.configure(bg="#2e2e2e")
    btn_bg = "#444"
    btn_fg = "white"
    default_font = ("Courier New", 12, "bold")

    title_instruction = Label(new_window, text="Enter Title of Account", bg=btn_bg, fg=btn_fg, font=default_font)
    title_input = Entry(new_window, width=35, border=8)

    username_instruction = Label(new_window, text="Enter Username", bg=btn_bg, fg=btn_fg, font=default_font)
    username_input = Entry(new_window, width=35, border=8)

    password_instruction = Label(new_window, text="Enter Password", bg=btn_bg, fg=btn_fg, font=default_font)
    password_input = Entry(new_window, width=35, border=8)
    
    button_first = Button(new_window, text="add account", width=35, bg=btn_bg, fg=btn_fg, font=default_font, command=lambda: input_function(title_input.get(), username_input.get(), password_input.get())) 
    
    delete_instruction = Label(new_window, text="Enter the Title of the Account\nyou want to delete:", bg=btn_bg, fg=btn_fg, font=default_font)
    delete_input = Entry(new_window, width=35, border=8)
    delete_btn = Button(new_window, text="Delete Account", command=lambda: delete_account(delete_input, delete_confirm), bg=btn_bg, fg=btn_fg, font=default_font)
    delete_confirm = Text(new_window, width=35, height=1, bg="gray", fg="black", font=("Courier New", 12, "bold"))

    close_btn = Button(new_window, text="Close", command=new_window.destroy, bg=btn_bg, fg=btn_fg, font=default_font)
#The Placement of the buttons on the first menu are formatted here.
#Second button removed. The second button function was moved into button_first for simplicity.
    title_instruction.grid(row=0, column=0, columnspan=4)
    title_input.grid(row=1, column=0, columnspan=4, pady=20, padx=20)

    username_instruction.grid(row=2, column=0, columnspan=4)
    username_input.grid(row=3, column=0, columnspan=4, pady=20, padx=20)

    password_instruction.grid(row=4, column=0, columnspan=4)
    password_input.grid(row=5, column=0, columnspan=4, pady=20, padx=20)

    button_first.grid(row=6, column=0, columnspan=4, padx=20, pady=10)

    delete_instruction.grid(row=7, column=0, columnspan=4, pady=25)
    delete_input.grid(row=8, column=0, columnspan=4, pady=15, padx=20)
    delete_btn.grid(row=9, column=0, columnspan=4, padx=20, pady=10)
    delete_confirm.grid(row=10, column=0, columnspan=4, padx=20, pady=10)

    close_btn.grid(row=11, column=0, columnspan=4, padx=25, pady=10)

    return title_input, username_input, password_input, delete_input

def view_accounts():
    new_window = Toplevel(root)  
    new_window.title("Account List")
    new_window.configure(bg="#2e2e2e")

    accounts_box = Text(new_window, width=60, height=25, bg="gray", fg="black", font=("Courier New", 12, "bold"))
    accounts_box.grid(row=0, column=0, pady=20)

    titles, usernames, passwords, accounts = read_columns("Password.csv")

    for t, u, p in zip(titles, usernames, passwords):
        accounts_box.insert("end", f"Title: {t} \nUsername: {u} \nPassword: {p}\n\n")

    accounts_box.configure(state="disabled")

def generate_1(user_input1, user_input2):
    output.configure(state="normal")
    output.delete("1.0", END)  

    if not user_input1.isdigit() or not user_input2.isdigit():
        output.insert("1.0", "A number must be entered", "center")
    else:
        char_count = int(user_input1)
        password_count = int(user_input2)
        generate_1_2(char_count, password_count)

    output.configure(state="disabled")  

def generate_2(user_input1, user_input2):
    output.configure(state="normal")
    output.delete("1.0", END)  

    if not user_input1.isdigit() or not user_input2.isdigit():
        output.insert("1.0", "A number must be entered", "center")  
    else:
        char_count = int(user_input1)
        password_count = int(user_input2)
        generate_2_2(char_count, password_count)

    output.configure(state="disabled")  
      

def generate_1_2(char_count, password_count):
    for outputs in range (password_count):
        #Because this is a for loop, randlist will need to be cleared everytime it starts.
        #This is required for making several passwords individually or they will stack on eachother.
        randlist.clear()
        #This for loop is for the individual password length. Char_count was the user input.
        for items in range (char_count):
            #with 80 list items in char_list, randselection finds a random number in this range.
            randselection = random.randint(0,79)
            #The previous random number is matched to the char_list1 list and a character is selected.
            get_rand_char = (char_list1[randselection])
            #The randlist will collect all the random chracters in char_list1 and save them here as a new list.
            randlist.append(get_rand_char)
        #This variable joins the seperated string character and forms the password.
        new_password ="".join(randlist)
        #The new password is appended/added to password output(outside of randlist). This is for saving txt files.
        password_output.append(new_password)
        output.configure(state="normal")
        output.insert("end", f"NEW PASSWORD: {new_password}\n", "center")
        output.configure(state="disabled")
def generate_2_2(char_count, password_count):
    for outputs in range (password_count):
        #Because this is a for loop, randlist will need to be cleared everytime it starts.
        #This is required for making several passwords individually or they will stack on eachother.
        randlist.clear()
        #This for loop is for the individual password length. Char_count was the user input.
        for items in range (char_count):
            #with 80 list items in char_list, randselection finds a random number in this range.
            randselection = random.randint(0,59)
            #The previous random number is matched to the char_list1 list and a character is selected.
            get_rand_char = (char_list2[randselection])
            #The randlist will collect all the random chracters in char_list1 and save them here as a new list.
            randlist.append(get_rand_char)
        #This variable joins the seperated string character and forms the password.
        new_password ="".join(randlist)
        #The new password is appended/added to password output(outside of randlist). This is for saving csv files.
        password_output.append(new_password)
        output.configure(state="normal")
        output.insert("end", f"NEW PASSWORD: {new_password}\n", "center")
        output.configure(state="disabled")

#This function adds user account title, username, and password.
def input_function( title_input, username_input, password_input):
    #Below condition describes 3a scenario where an empty value is entered.
    if title_input.strip() == '':
        print("A title is required.")
        #The username and password are only requested as input if a title is created.
    #All (3) inputs are appended to their appropriate list below. The title (of account) is used to identify the information else where in the program.
    else:
        title.append(title_input)
        username.append(username_input)
        password.append(password_input)
        #The program checks here if the file named Password.csv exists. It must exist in order to save the information
        # for later use in the program
        #This is made as a variable to be used in a conditional statement.
        file_check = os.path.isfile("Password.csv")
        #The below syntax opens Password.csv. If the file does not exist already, it is created.
        #The "a" represents an append attribute that adds information to the file.
        #'newline' will ensure data is written on a new line. A new cell is written in the csv file with a newline.
        with open("Password.csv", "a", newline='') as file:
            #This variable uses a writing method for csv files. This will handle formatting for the file type.
            writer = csv.writer(file)
            #Below is a condition that creates headers in the top columns for values represented by lists in this program.
            #This are only created when the file does not exist.
            if not file_check:
                writer.writerow(["Title", "Username", "Password"])
            #This 'for' loop formats how information is displayed/written.
            # 'i' represents the item position/index in each list. When the file gets information added, the commas indicate
            # every new cell to add information to. With every item 'i' representing the item's position, it will write the first items in
            # one row, second items in next row, and so on. This step is critical for organizing how information is displayed.
            for i in range(len(title)):
                writer.writerow([title[i], username[i], password[i]])

#The early version of this program used a .txt file called "Passwords.txt". The 'filename' variable is used an argument in several functions.
# Deleting this argument from the function's arguments will cause an error and halt the program (corrupted encryption). It is not yet clear why this happens.
#This variable is a work-around but doesn't actually get used. The 'with open' syntax does the actual work of manipulating the csv file.
#Deleting this variable also doesn't affect the functions with the argument shown.
filename = "Password.csv"

#The CSV file has (3) columns for Title, Username, and Passwords. This function reads the CSV file columns.
#This function is used in view_accounts()
def read_columns(filename):
    #The items are appended to these lists for the user to view the output.
    titles = []
    usernames = []
    passwords = []
    accounts = []
    #Logic for reading csv file. 
    with open(filename, "r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            titles.append(row["Title"])
            usernames.append(row["Username"])
            passwords.append(row["Password"])
            accounts.append(row)
    return titles, usernames, passwords, accounts
#This function is used in delete_account_by_title. the logic is based on 
def read_accounts(filename):
    accounts = []
    with open("Password.csv", "r", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts.append(row)
    return accounts
 
#This function gives a response to the user if deletion was successful or failed.
def delete_account(delete_input, delete_confirm):
    #User inputs title (of username and password) to delete.
    title_to_delete = delete_input.get().strip()
    #title_to_delete logic is applied to csv file. This variable will have (2) outcomes.
    deleted = delete_account_by_title("Password.csv", title_to_delete)
    delete_confirm.configure(state="normal")
    delete_confirm.delete("1.0", "end")
    #If the title was deleted, a conformation will appear.
    if deleted:
        delete_confirm.insert("end", f"Deleted account: {title_to_delete}")
        delete_input.delete(0, "end")
        delete_confirm.configure(fg="black")
    #The else condition gives an output that does not find the title that user was trying to delete.
    else:
        delete_confirm.insert("end", f"No account found with title: {title_to_delete}")
        #This line of code was to originally have red text, but was set to black for a better contrast.
        #Changing again in the future requires changing background color of widget/box.
        delete_confirm.configure(fg="black")
    #Conformation message cannot be changed by user.
    delete_confirm.configure(state="disabled")

#This function shows how a a title is filtered out from the data.
def delete_account_by_title(filename, title_to_delete):
    #accounts are read using the read_accounts function. The data is assigned to a variable.
    accounts = read_accounts(filename)
    #This logic was the result of troubleshooting.
    #All possibilities for finding account information is done to find information related to 'Title' items.
    #the title_to_delete syntax is to prevent a previous error from occuring>>> Leave this.
    updated_accounts = [account for account in accounts if account["Title"] != title_to_delete]

    #This conditional statement compares the actual list of accounts (in title list) to the previous list.
    #If there is no change between the actual list, and new list (where an account got deleted) it returns as false.
    if len(accounts) == len(updated_accounts):
        return False

    #In the circumstance where the updated list is changed, it is rewritten to the csv file with the new data.
    with open(filename, "w", newline='') as file:
        fieldnames = ["Title", "Username", "Password"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_accounts)
    #This returns the new values back into the environment of the program and it can keep being used.
    return True 

#Symmetric Key generated from a seperate python file.
#Generated key saved as .key file and is sitting in the same directory as this program.
#The Cryptography library handles the key for decrypting the encrypted file.
#'rb' is 'Read Binary' and any change in the files or key may corrupt the files.
def key_loader():
    with open('mykey.key', 'rb') as key_file:
        return key_file.read()
    
#Key_loader is called to decrypt file.
def decrypt_file():
    #key loader is assigned to the key variable.
    key = key_loader()
    #Fernet (from cryptography library) handles the information in the .key file.
    #order of events: .key file > key_loader() > 'key' variable > Fernet(key) handling > f variable
    f = Fernet(key)
    #Encrypted file is opened here and information is read.
    with open('Password.csv', 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    #Below variable decrypts data using the 'f' variable which has the key. Decrypt method is called.
    decrypted_data = f.decrypt(encrypted_data)
    #Decrypted data is written back into the csv file and can now be read and edited freely.
    with open('Password.csv', 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

#The reverse order of the decrypted function is done here to encrypt the information.
def encrypt_file():
    key = key_loader()
    f = Fernet(key)
    #plain text binary data is read.
    with open('Password.csv', 'rb') as file:
        original_data = file.read()
    #Using the key in the 'f' variable(key), the encrypt method is used to scramble the plain text data.
    encrypted_data = f.encrypt(original_data)
    #Encrypted data is written to csv file.
    with open('Password.csv', 'wb') as file:
        file.write(encrypted_data)

#This function is the most critical piece of code in the program.
#Before the root window close (main window) the encrypt function is called before close the window.
#The close button in the root window is tied to this function.
def encrypt_and_close(root):
    #Encrypt function called.
    encrypt_file()
    #Window is then allowed to close
    root.destroy() 

#When the program is opened, the first function called decrypts the csv file.
decrypt_file()

#Thes variables are for the buttons in the first menu in the GUI.
#Sizing, properties, and logic of these buttons are here.
button_first = Button(root, text="Password Generator", height=4, width=60,
                      bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, activeforeground=btn_fg, 
                      font=default_font, command=password_gen1) 
button_third = Button(root, text="More Info On Passwords ", height=4, width=60,
                      bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, activeforeground=btn_fg, 
                      font=default_font, command=sos) 
button_fourth = Button(root, text="Password Manager", height=4, width=60,
                      bg=btn_bg, fg=btn_fg, activebackground=btn_active_bg, activeforeground=btn_fg, 
                      font=default_font, command=password_manager)
close_btn = Button(root, text="Close", command=lambda: encrypt_and_close(root), bg=btn_bg, fg=btn_fg, font=default_font)

#The Placement of the buttons on the first menu are formatted here.
#Second button removed. The second button function was moved into button_first for simplicity.
button_first.grid(row=1, column=0, columnspan=4, padx=10, pady=(15, 1))
button_third.grid(row=2, column=0, columnspan=4, padx=10, pady=1)
button_fourth.grid(row=3, column=0, columnspan=4, padx=10, pady=(1, 15))
close_btn.grid(row=4, column=0, columnspan=4, padx=10, pady=10)


#*** DO NOT CHANGE *** This function is what keeps the GUI window continuously working.
root.mainloop()
