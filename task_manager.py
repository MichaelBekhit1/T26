import mysql.connector
import string
import hashlib
import datetime

# Perhaps this connection should be elsewhere in the program stylistically? The functions depend on it.
# Connects program to database with code_reviewer connection. This connection is insecure.

user_database = mysql.connector.connect(
    host = "localhost",
    user = "code_reviewer",
    password = "code123",
    database = "26_capstone_iii"
    )

# code_reviewer has DB privileges only
# There is no sql server attached to course. The DB is on my local server and does not allow remote access so I will be marked on syntax.

current_date = datetime.datetime.now()
current_date = str(current_date.strftime("%Y-%m-%d"))
cursor = user_database.cursor(buffered = True) # buffered = True was a fix for a problem. Note: Figure out what is going on here.

# I am intending to use this so that a person accessing the database cannot credentials in plain text to lists although they could still be added to hash tables

def hash_and_digest(string):
    return (hashlib.sha1(string.encode())).hexdigest()

def valid_username_to_register():

    number_of_attempts = 3
    mistake_count = 0
    minimum_length = 4

    # checks username is {minimum length} or more characters long and is not already taken. If input is invalid, input is requested again. {number of attempts} are allowed.
    

    for _ in range(number_of_attempts):

        username = input("Please enter the username for the user that you wish to register: ")
        cursor.execute(f"SELECT username FROM 26_capstone_iii.user_credentials WHERE username = '{username}';")
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


def valid_password_to_register():

    number_of_attempts = 3
    mistake_count = 0
    minimum_length = 8
    punctuation_count = 0
    minimum_punctuation_count = 1

    
    for _ in range(number_of_attempts):

    # checks password is  {minimum length} and has {minimum punctuation count} punctuation chars. {number of attempts} attempts are allowed.

        password = input("Please enter the password for the user that you wish to register: ")
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
    WHERE (username = '{username_input}' AND password = '{hash_and_digest(password_input)}');""")
    value = cursor.fetchone()
    if value != None:
        return True
    else:
        print("Invalid login. Please try again.")
        return False
    

def register_user(valid_username, valid_password): # note that these should been validated using the appropriate functions but currently that is not controlled behaviour 
    
    # Injection attack - escape the characters

            sql = "INSERT INTO user_credentials (username, password) VALUES (%s,%s);"
            cursor.execute(sql, (valid_username, hash_and_digest(valid_password)))
            user_database.commit()
            print("The user has been registered successfully.")
            
      
def register_task():

    title = input("Please enter the title of the task: ")
    description = input("Please describe the task: ")
    date_assigned = input("Please input the date in the required format( e.g. 17 Jan 2022): ") # these date inputs could have some validation
    date_due = input("Please enter the date the task is due for completion in the required format(YYYY-MM-DD include '-'): ")
    assigned_user_id = input("Please enter the id of the user you wish to assign the task to: ") # this is not very flexible. offer another option
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
        assigned user: {assigned_user_id}
        
        If you wish to proceed please enter 'y' or, to exit, press any key: 
        """)

    if proceed != "y":
            exit()
    else:

        sql = "INSERT INTO 26_capstone_iii.tasks (title, description, date_assigned, date_due, user_id) VALUES (%s, %s, %s, %s, %s)"
        # The following are all visible in plain text format inside the database - context may require adjustment    
        cursor.execute(sql, (title, description, date_assigned, date_due, assigned_user_id))
        user_database.commit()
        print("The user has been registered successfully.")

def view_my_tasks(username):
    cursor.execute(f"SELECT user_id FROM user_credentials WHERE username = '{hash_and_digest(username)}';")
    user_id = cursor.fetchone()
    cursor.execute(f"SELECT task title, task description, date due FROM tasks WHERE user_id = '{user_id}';")
    my_tasks = cursor.fetchall()
    print(my_tasks)

def view_all_tasks():
    cursor.execute(f"SELECT task title, task description, date due FROM tasks")
    all_tasks = cursor.fetchall()
    print(all_tasks)

def generate_reports(username):
    if username == "admin": # needs changing if there are multiple administrators. Analysis needed but probably change it anyway to cater for that possibility.
        with open("task_overview.txt", "w+") as task_overview:
            cursor.execute("SELECT COUNT(*) FROM tasks")
            task_count = cursor.fetchone()
            task_count = task_count[0] # convert from tuple to int
            task_overview.write(f"The total number of tasks is: {task_count}\n")
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE (completed = '0')")
            incomplete_task_count = cursor.fetchone()
            incomplete_task_count = incomplete_task_count[0] # convert from tuple to int
            task_overview.write(f"The number of incomplete tasks is {incomplete_task_count}\n")
            cursor.execute("SELECT COUNT(*) FROM tasks WHERE (completed = '1')")
            complete_task_count = cursor.fetchone()
            complete_task_count = complete_task_count[0] # convert from tuple to int
            task_overview.write(f"The number of complete tasks is {complete_task_count}\n")
            cursor.execute(f"SELECT COUNT(*) FROM tasks WHERE (date_due < {current_date})")
            overdue_task_count = cursor.fetchone()
            overdue_task_count = overdue_task_count[0] # troubleshooting. This doesnt work for completed 'overdue' tasks
            task_overview.write(f"The number of tasks that are currently overdue is {overdue_task_count}\n")
            task_overview.write(f"The percentage of tasks that are incomplete is {(incomplete_task_count/task_count)*100}\n")
            task_overview.write(f"The percentage of tasks that are overdue is {(overdue_task_count/task_count)*100}\n")
    else:
        print("This option is only available to a user with administrative privilege.")

def display_statistics(username):
    if username == "admin": # needs changing if there are multiple administrators. Analysis needed but probably change it anyway to cater for that possibility.
        with open("user_overview.txt", "w+") as user_overview:
            cursor.execute("SELECT COUNT(*) FROM user_credentials")
            total_users = cursor.fetchone()
            total_users = total_users[0]
            cursor.execute("SELECT user_id FROM user_credentials")
            user_list = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) FROM tasks")
            task_count = cursor.fetchone()
            task_count = task_count[0] # convert from tuple to int
            
            for user_id in user_list:

                cursor.execute(f"SELECT * from tasks WHERE user_id = '{user_id[0]}'")
                task_information = cursor.fetchall()
                print(f"USER {user_id} has the following tasks: {task_information}")
                cursor.execute(f"SELECT COUNT(*) FROM tasks WHERE user_id ='{user_id[0]}'")
                task_count_for_user = cursor.fetchone()
                print(f"The number of tasks assigned to {user_id} is {task_count_for_user}")
                print(f"The percentage of tasks assigned to this user is {(task_count_for_user/task_count) *100}")
                cursor.execute(f"SELECT COUNT(*) FROM tasks WHERE (date_due < {current_date})")
                

            user_overview.write(f"The total number of users registered is {total_users}\n")
            cursor.execute("SELECT COUNT(*) FROM tasks")
            task_count = cursor.fetchone()
            task_count = task_count[0] # convert from tuple to int
            user_overview.write(f"The total number of tasks is: {task_count}\n")
            

    else:
        print("This option is only available to a user with administrative privilege.")


       






def main():

    # Return the user to the menu to complete further actions but to check that their authorisation has not been removed since their last action.

    menu = ""
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    while validate_login(username, password) == True and menu != "7":
        menu = input("""
        Please enter a number to select from the following options:
        
        1 Register a new user
        2 Register a new task
        3 View tasks assigned to me
        4 View all tasks
        5 Generate reports
        6 Display Statistics
        7 Exit program



        

        """).lower()

        if menu == "1":
            username_to_register = valid_username_to_register()
            password_to_register = valid_password_to_register()
            register_user(username_to_register, password_to_register)

        elif menu == "2":
            register_task()
        
        elif menu == "3":
            view_my_tasks(username)
            intention_mark_complete = input("Please select 1 to mark a particular task as complete, 2 to exit the program or any key to return to menu. ")
            if intention_mark_complete == "1":
                task_id_to_complete = input("Please enter the ID of the task that you wish to mark as complete: ")
                cursor.execute(f"UPDATE tasks SET completed = 1 WHERE id = '{task_id_to_complete}'")
                user_database.commit()
            elif intention_mark_complete == "2":
                exit()



        elif menu == "4":
            view_all_tasks()
        
        elif menu == "5":
            generate_reports(username)

        elif menu == "6":
            display_statistics(username)

        elif menu == "7":
            exit()

        else:
            print("You have made an invalid selection")

if __name__ == "__main__":
    main()


    

# close cursor and database to free up resources

cursor.close()
user_database.close()

