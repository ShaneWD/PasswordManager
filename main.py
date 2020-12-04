# pip install mysql-connector-python
# pip install pycryptodome
# pip install bcrypt

from Crypto.Cipher import AES
import bcrypt
import mysql.connector
from os import path
from Crypto.Util.Padding import pad  # for encrypting
from Crypto.Util.Padding import unpad
import random

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
        if 20 > len(password) > 5:
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

        elif len(password) <= 5:
            print("Password is too short")
            create_account()
        elif len(password) >= 20:
            print("Password is too large")
            create_account()
    else:
        print("Invalid username length. Try again")
        create_account()


def store_password():
    username = input("""Username
    >""")
    mycursor.execute(f"""SELECT * FROM accounts WHERE username = '{username}' """)
    myresult = mycursor.fetchone()
    hashed_password = myresult[2].encode('utf-8')
    password = input("""Password
    >""")
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        account_id = myresult[0]
        location = input("""Website name
    >""")
        sub_username = input("""What is your username for that website?
    >""")
        the_password = input("""What is your password for that website?
    >""")
        notes = input("""Any personal notes (DO NOT include confidential information) """)

        salt = random.randint(9999, 99999)
        salt = "salt" + str(salt)
        pwd_salt = the_password + salt
        if account_id != "" and location != "" and sub_username != "" and the_password != "":
            mycursor.execute(f""" 
INSERT INTO stored_passwords (account_id, location, notes, the_password, username, salt, website_username) 
VALUES ("{account_id}", "{location}", "{notes}", aes_encrypt("{pwd_salt}", "{password}"), "{username}", "{salt}",
"{sub_username}");""")
            mydb.commit()
    else:
        print("failure")


def read_password():
    username = input("""Username
    >""")
    mycursor.execute(f"""SELECT * FROM accounts WHERE username = '{username}' """)
    myresult = mycursor.fetchone()
    hashed_password = myresult[2].encode('utf-8')
    password = input("""Password
    >""")
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        account_id = myresult[0]
        location = input("""Website name
    >""")
        mycursor.execute(f"""
SELECT *, REPLACE(CAST(AES_DECRYPT(the_password,'{password}') as char(10000)), salt, ""), salt
FROM stored_passwords WHERE username = '{username}' AND location = '{location}';
""")
        myresult = mycursor.fetchone()
        print(f"""
Website Name: {myresult[0]}
Website Username: {myresult[6]}
Website Password: {myresult[7]}
Notes: {myresult[3]}
""")
    else:
        print("Failure")


create_account()
