# pip install mysql-connector-python
# pip install pycryptodome
# pip install bcrypt

from Crypto.Cipher import AES
import bcrypt
import mysql.connector
from os import path
from Crypto.Util.Padding import pad # for encrypting
from Crypto.Util.Padding import unpad


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
        if len(password) == 17:
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

        key = password.encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC)
        plaintext = the_password.encode('utf-8')
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        with open('cipher_file', 'wb') as c_file:
            c_file.write(cipher.iv)
            c_file.write(ciphertext)
        file_pwd = open("cipher_file", "r")
        pwd = (file_pwd.read())

        if account_id != "" and location != "" and sub_username != "" and the_password != "":
            mycursor.execute(f""" 
            INSERT INTO stored_passwords (account_id, location, notes, the_password, username) 
            VALUES ("{account_id}", "{location}", "{notes}", "{pwd}", "{username}");""")

            mydb.commit()
    else:
        print("failure")


store_password()


