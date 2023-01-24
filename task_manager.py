import mysql.connector
import string
import hashlib

# Connects program to database with code_reviewer connection. This connection is insecure.

user_database = mysql.connector.connect(
    host = "localhost",
    user = "code_reviewer",
    password = "code123",
    database = "26_capstone_iii"
    )

# code_reviewer has DB privileges only
# There is no sql server attached to course. The DB is on my local server and does not allow remote access so I will be marked on syntax.

cursor = user_database.cursor(buffered = True) # buffered = True was a fix for a problem. Note: Figure out what is going on here.



def valid_username():

    number_of_attempts = 3
    mistake_count = 0
    minimum_length = 4

    # checks username is {minimum length} or more characters long and is not already taken. If input is invalid, input is requested again. {number of attempts} are allowed.
    

    for _ in range(number_of_attempts):

        username = input("Please enter your username: ")
        cursor.execute(f"SELECT username FROM 26_capstone_iii.user_credentials WHERE username = '{(hashlib.sha1(username.encode())).hexdigest()}';")
        name = cursor.fetchone()

        if mistake_count >= (number_of_attempts -1):
            print("You have had too many unsuccessful attempts.")
            exit()
        elif name != None:
            print("That username is already taken. Please try again.")
            mistake_count += 1
        elif len(username) < minimum_length:
            print(f"Your username must be at least {minimum_length} characters long. Please try again")
            mistake_count += 1
        else:
            return username


def valid_password():

    number_of_attempts = 3
    mistake_count = 0
    minimum_length = 8
    punctuation_count = 0
    minimum_punctuation_count = 1

    
    for _ in range(number_of_attempts):

    # checks password is  {minimum length} and has {minimum punctuation count} punctuation chars. {number of attempts} attempts are allowed.

        password = input("Please enter your password: ")
        confirm_password = input("Please reenter the password for the user that you wish to register: ")
        
        for punctuation_char in range(len(string.punctuation)):
            for char in range(len(password)):
                if password[char] == string.punctuation[punctuation_char]:
                    punctuation_count += 1

        if mistake_count >= (number_of_attempts -1):
                print("You have had too many unsuccessful attempts.")
                exit()

        elif password != confirm_password:
            print("Your passwords do not match. Please try again.")
            mistake_count += 1

        
        elif len(password) < minimum_length:
                print(f"Your password must be at least {minimum_length} characters long. Please try again")
                mistake_count += 1

        elif punctuation_count >= minimum_punctuation_count:
            print("""Your password must contain one of the following characters: !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~""")

        else:
            return password

def register_user(valid_username, valid_password):
    
    # Injection attack vulnerability dealt with by hashing the username

            cursor.execute(f"""
            INSERT INTO user_credentials (username, password)
            VALUES ('{(hashlib.sha1(valid_username.encode())).hexdigest()}', '{(hashlib.sha1(valid_password.encode())).hexdigest()}');
            """)
            user_database.commit()
            print("The user has been registered successfully.")
            
        
    

def validate_login(username_input, password_input):

    # Filter the table for the given username and password and return the username if they are present. If they are not present the login is not valid

    cursor.execute(f"""
    SELECT username FROM 26_capstone_iii.user_credentials 
    WHERE (username = '{(hashlib.sha1(username_input.encode())).hexdigest()}' AND password = '{(hashlib.sha1(password_input.encode())).hexdigest()}');""")
    value = cursor.fetchone()
    if value != None:
        return True
    else:
        return False
    
# The intention here is to return the user to the menu to complete further actions but to check that their authorisation has not been removed since their last action.

menu = ""

while validate_login(valid_username(), valid_password()):
    pass





cursor.close()
user_database.close()

