import mysql.connector

user_database = mysql.connector.connect(
    host = "localhost",
    user = "code_reviewer",
    password = "code123"
)

print(user_database)

