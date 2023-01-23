import mysql.connector

# Connects program to database with code_reviewer connection. This connection is insecure.

user_database = mysql.connector.connect(
    host = "localhost",
    user = "code_reviewer",
    password = "code123",
    database = "26_capstone_iii"
    )

# code_reviewer has DB privileges only
# There is no sql server attached to course. The DB is on my local server and does not allow remote access so I will be marked on syntax.

cursor = user_database.cursor()


def register_user():
    user = input("Please enter the username of the user that you wish to register: ")
    passw = input("Please enter the password for the user that you wish to register: ")
    confirm_password = input("Please reenter the password for the user that you wish to register: ")
    if passw == confirm_password:
        cursor.execute(f"""
        INSERT INTO user_credentials (username, password)
        VALUES ('{user}', '{passw}');
        """)

def validate_login(username, password):
    for user, pword in cursor.execute("SELECT username, password FROM user_credentials"):
        if username == user and password == pword:
            return True
        else:
            return False

# validate_login("my_username", "my_password")

register_user()