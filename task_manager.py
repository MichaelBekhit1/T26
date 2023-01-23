import mysql.connector

user_database = mysql.connector.connect(
    host = "localhost",
    user = "code_reviewer",
    password = "code123",
    database = "26_capstone_iii"
    )

# code_reviewer has DB privileges only
# There is no sql server attached to course. The DB is on my local server.

cursor = user_database.cursor()

def login(username, password):
    pass

username_list = cursor.execute("SELECT username FROM user_credentials")
print(username_list)