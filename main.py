# pip install mysql-connector-python
# pip install pycryptodome
# pip install bcrypt

from Crypto.Cipher import AES
import bcrypt
import mysql.connector
from os import path


file_pwd = open("pwd.txt", "r")
# "pwd.txt" has plain text password for the database.
pwd = (file_pwd.read())
# "pwd.txt" will not be included in GitHub for security reasons.
file_pwd.close()
# close unneeded process to same more memory.
mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password=pwd,
                               database='pwd_manager')
mycursor = mydb.cursor()


def create_account():
    username = input("""Username
>""")
    if 3 < len(username) < 15:
        password = input("""Password
>""")
        if 5 < len(password) < 15:
            password = password.encode('utf-8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
            hashed = hashed.decode()
            print(hashed)
            mycursor.execute("""SELECT MAX(account_id) FROM accounts""")
            # retrieves the row with the highest message_id number
            old_max_id = mycursor.fetchone()
            try:
                new_max_id = old_max_id[0] + 1
                # creates the highest id number that is one larger from the second largest.
            except TypeError:
                new_max_id = 1
                # used for if the database has no rows/is wiped clean

            mycursor.execute(f""" 
INSERT INTO accounts (account_id, username, the_password) 
VALUES ("{new_max_id}", "{username}", "{hashed}");""")

            mydb.commit()

        else:
            create_account()
    else:
        create_account()


create_account()


