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
    

def register_user(valid_username, valid_password): # note that these should been validated using the appropriate functions - Is there a token facility for this? 
    
    # Injection attack vulnerability dealt with by hashing the username

            cursor.execute(f"""
            INSERT INTO user_credentials (username, password)
            VALUES ('{(hashlib.sha1(valid_username.encode())).hexdigest()}', '{(hashlib.sha1(valid_password.encode())).hexdigest()}');
            """)
            user_database.commit()
            print("The user has been registered successfully.")
            
      
# The intention here is to return the user to the menu to complete further actions but to check that their authorisation has not been removed since their last action.

def register_task():

    title = input("Please enter the title of the task: ")
    description = input("Please describe the task: ")
    date_assigned = input("Please input the date in the required format( e.g. 17 Jan 2022): ") # these date inputs could have some validation
    date_due = input("Please enter the date the task is due for completion in the required format(e.g. 17 Jan 2022")
    assigned_user_id = input("Please enter the id of the user you wish to assign the task to: ")
    cursor.execute(f"SELECT username FROM 26_capstone_iii.user_credentials WHERE (user_id = '{assigned_user_id}');")
    returned_username = cursor.fetchone()

    if returned_username == None:
        print("You have entered a user_id that is not recognised.")
        proceed = input("If you wish to proceed with registration of the task without a user_id please enter 'y' or to exit, press enter: ")
    else:
        proceed = input(f"""
        The task that you have entered is as follows:
        title: {title}
        description: {description}
        date assigned: {date_assigned}
        date due: {date_due}
        assigned user: {assigned_user_id} {returned_username}
        
        If you wish to proceed please enter 'y' to exit, press enter: 
        """)

    if proceed != "y":
            exit()
    else:

        # Injection attack defence - placeholder accepts data type string and data type int accordingly. Note: More research.

        sql = "INSERT INTO 26_capstone_iii.tasks (title, description, date_assigned, date_due, user_id) VALUES (%s, %s, %s, %s, %d)"
        cursor.execute(sql, (title, description, date_assigned, date_due, assigned_user_id))
        user_database.commit()
        print("The user has been registered successfully.")

menu = ""

while validate_login(valid_username(), valid_password()) and menu != "e":
    pass





cursor.close()
user_database.close()

