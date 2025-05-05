'''
Author: Jimmy Torres
Last Date edited:7/3/2025
Created:7/3/2025

Program:Password Generator

Note: The purpose of this program is to generate a random password. The password length
and criteria will be selected by the user.

'''
#Random class is required for password generation.
import random
#datetime will be used for exporting passwords to a txt file if needed. This is added to .txt file name.
import datetime

#All characters in lists are keyboard characters.

#80 characters in char_list1. This includes special characters.
char_list1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
              'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 
              'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 
              'z', 'x', 'c', 'v', 'b', 'n', 'm', 
              'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 
              'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 
              'Z', 'X', 'C', 'V', 'B', 'N', 'M', 
              '~', '!', '@', '#', '$', '%', '^', '&',
              '*', '(', ')', '-', '=', '_', '+',
              '[', '{', ']', '}', '\\', '|', ';', ':',
              "'", '"', ',', '.', '<', '.', '>', '/', '?' ]
#60  characters in char_list2. This does not include Special Characters.
char_list2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
              'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 
              'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 
              'z', 'x', 'c', 'v', 'b', 'n', 'm', 
              'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 
              'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 
              'Z', 'X', 'C', 'V', 'B', 'N', 'M',]
#This list will be used to store the individually generated characters of each password.
#This also gets cleared with every password iteration.
randlist = []
#Joined characters will create an output(password) and be saved here. 
new_password = []
#This list serves as the content needed to write and save new .txt files.
password_output = []

#Menu function is for the user to navigate the different password generators. Guidance provided.
def menu():
    print("--------------------------------------------------------")
    print("The following program will create a password (or several). \n Type and enter one of the choices:")
    print("'1' --- Include all characters on keyboard.")
    print("'2' --- Use only numbers and letters.")
    print("'sos' --- For more info on password creation.")
    #User input is done here.
    user_input = (input("Your response:   "))
    #To avoid possible issues with undefined inputs, the user is limited to '1', '2', or 'sos'.
    #Other inputs restart the loop.
    while True:
        #'1' selects password generation with special characters.
        if user_input == "1":
            password_special_char()
        #'2' selects password generation with no special characters.
        elif user_input == "2":
            password_no_special_char()
        #'sos' gives further information to the user about how many passwords are possible w/ their selection.
        elif user_input == "sos":
            #Last reasearched and calculated on 4/3/2025.
            print("--------------------------------------------------------")
            print("CISA as of 2025 recommends using a password of 16 characters.\n")
            print("This guidance means option 1 will give you:")
            print("80^16 or 115.29 octillion possibilities.\n")
            print("Option '2' will give you:")
            print("60^16 or 4.4 septillion possibilities.(Less than option 1)")
            input("Press any key to return to menu")
            #Restarts menu function for user to make an informed selection.
            menu()
        #Bad inputs are caught here. The user is made aware and must manually restart the menu w/ an input.
        else:
            print("Whoops! enter one of the menu items.")
            input("Press any key to continue")
            menu()
            
 #This function creates the password with special charcters.       
def password_special_char():
    print("--------------------------------------------------------")
    #This is the password length. While true is necessary to ensure a specific condition is met with numbers.
    while True:
        #User input is asked for here.
        char_count = input("We'll generate a password WITH special characters. \nPlease enter how many characters you need in your password:   ")
        #Because there is no method to check integers, digits/numbers are checked in in the string first.
        if char_count.isdigit():
            #Char_count is converted to integer after digits/numbers were accepted.
            char_count = int(char_count)
            #User is made aware of how long password will be.
            print(f"Generated Password will be made with {char_count} characters.")
            print("--------------------------------------------------------")
            break
        #All other string values are caught here and user must re-enter an digit/number. 
        else:
            print("--------------------------------------------------------")
            print("A number must be entered.")
            print("--------------------------------------------------------")
    #Password amount will tell program to generate 'x' amount of times.
    while True:
        password_amount = input("how many passwords do you need? \nQuantity:   ")
        #Because there is no method to check integers, digits/numbers are checked in in the string first.
        if password_amount.isdigit():
            #Char_count is converted to integer after digits/numbers were accepted.
            password_amount = int(password_amount)
            #User is made aware of how long password will be.
            print(f"{password_amount} passwords will be generated.")
            print("--------------------------------------------------------")
            break
        #All other string values are caught here and user must re-enter an digit/number. 
        else:
            print("--------------------------------------------------------")
            print("A number must be entered.")
            print("--------------------------------------------------------")
        #Password amount will tell program to generate 'x' amount of times.
        print("--------------------------------------------------------")
    #In this for loop, the password_amount input will define how many times(passwords) to make.
    for outputs in range (password_amount):
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
        
        #New password shown. This is still in a loop and will repeat until all passwords are generated.
        print(f"NEW PASSWORD: \n{new_password} \n")
    #User is asked if they want to save the passwords outside of the program.    
    print("Did you want to save this password in a text file? Y/N ")
    print("--------------------------------------------------------")
    #While the user is only inputting 'y' or 'n' inputs:
    while True:
        #variable will lowercase user input to match a condition in the next while loop.
        #***Debugged*** Must be in while loop, outside will cause infinite loop.
        user_save = input("Your response:   ").lower()
        #Yes will start a with open loop that will write .txt files that  are time stamped.
        if user_save == "y":
            #'now' variable will capture current time.
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
            #***This was a debugged step*** With open is needed to control the closing of file-process. This will 'write' a new file.
            #'Password' naming convention be used on all new password files with a time stamp to avoid unsaved files.
            with open(f"Password{now}.txt", "w") as file:
                #This will be at the top of the .txt file.
                file.write("Passwords Generated:\n")
                #This for loop will go through every item in password output (secondary list from password generation).
                for password in password_output:
                    #Password is written with this line of code.
                    file.write(f"{password}\n")
                #File is closed to 'safely'/correctly save what was written.
                file.close()
                #User is given guidance on the remaining options they have with the program.
                input("Press any key to return to menu or close this window.")
                menu()
        #If user does not want to save their password to .txt file, they are given the same guidance as last comment.
        elif user_save == "n":
            input("Press any key to return to the menu. \nOtherwise, close this window to exit program.")
            menu()
        #Bad inputs are caught here.    
        else:
            print("Whoops! Please enter 'y' or 'n'.")
            
#***The below function is almost identical to the above function with exception of the characters list being used.
#Scroll through for more comments.            
def password_no_special_char():
    print("--------------------------------------------------------")
    while True:
        char_count = input("We'll generate a password WITH special characters. \nPlease enter how many characters you need in your password:   ")
        if char_count.isdigit():
            char_count = int(char_count)
            print(f"Generated Password will be made with {char_count} characters.")
            print("--------------------------------------------------------")
            break
        else:
            print("--------------------------------------------------------")
            print("A number must be entered.")
            print("--------------------------------------------------------")
    while True:
        password_amount = input("how many passwords do you need? \nQuantity:   ")
        if password_amount.isdigit():
            password_amount = int(password_amount)
            print(f"{password_amount} passwords will be generated.")
            print("--------------------------------------------------------")
            break 
        else:
            print("--------------------------------------------------------")
            print("A number must be entered.")
            print("--------------------------------------------------------")
    for outputs in range (password_amount):
        randlist.clear()
        for items in range (char_count):
            #Different range for non-special character list set here.
            randselection = random.randint(0,59)
            #Second character list with no special characters called here.
            get_rand_char = (char_list2[randselection])

            randlist.append(get_rand_char)

        new_password ="".join(randlist)
        password_output.append(new_password)

        print(f"NEW PASSWORD: \n{new_password} \n")
        print("--------------------------------------------------------")
    print("Did you want to save this password in a text file? Y/N")
    print("--------------------------------------------------------")
    
    while True:
        user_save = input("Your response:   ").lower()
        if user_save == "y":
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
            with open(f"Password{now}.txt", "w") as file:
                file.write("Passwords Generated:\n")
                for password in password_output:
                    file.write(f"{password}\n")
                file.close()
                input("Press any key to return to menu or close this window.")
                menu()
        elif user_save == "n":
            input("Press any key to return to the menu. \nOtherwise, close this window to exit program.")
            menu()
        else:
            print("Whoops! Please enter 'y' or 'n'.")

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    file = open(f"Password{now}.txt", "w")
    
    file.write("Passwords Generated:")
    file.write(f"{new_password}")
    file.close()

#User will see comment with information regarding how updated program is (if run directly).
def directstatement():
    print("Last edited on 4/3/2025 by Jimmy T.")

#This line of code is used to run script directly from local directory. Users do not need to load python to run.
if __name__ == "__main__":
    directstatement()

