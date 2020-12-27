import sqlite3
import random
import string
import bcrypt
from AES_encryption import encrypt as aes_encrypt, decrypt as aes_decrypt
# pip install -r requirements.txt
# for this file, MySQL is NOT needed.

mydb = sqlite3.connect('SQLite_PWD.db')

mycursor = mydb.cursor()
'''
mycursor.execute("""CREATE TABLE accounts (
        account_id INT NOT NULL UNIQUE PRIMARY key,
        username TEXT NOT NULL,
        password TEXT NOT NULL
                )""")
'''
'''
mycursor.execute("""CREATE TABLE stored_passwords (
        account_id INT NOT NULL REFERENCES accounts(account_id),
        username TEXT NOT NULL,
        location TEXT NOT NULL,
        website_username TEXT NOT NULL,
        the_password TEXT NOT NULL,
        salt TEXT NOT NULL,
        notes TEXT NULL
                )""")
'''
# account_id, location, notes, the_password, username, salt, website_username
# mycursor.execute("INSERT INTO accounts VALUES ('1', 'delete', 'delete' )")
# mycursor.execute("SELECT * FROM ACCOUNTS")
# data = mycursor.fetchall()

# mydb.commit()


def create_account():
    username = input("""Username
    >""").lower()
    if 3 < len(username) < 15:
        mycursor.execute(f"""SELECT username FROM accounts WHERE username = '{username}' """)
        myresult = mycursor.fetchone()
        # in order to see if that username already exists in the database
        if not myresult:
            password = input("""Password
    >""")
            if 20 > len(password) > 5:
                def get_random_string(length):
                    # Random string with the combination of lower and upper case
                    letters = string.ascii_letters
                    result_str = ''.join(random.choice(letters) for i in range(length))
                    return result_str

                salt_letter = get_random_string(12)
                salt_number = random.randint(99999999999, 999999999999)
                salt = salt_letter + str(salt_number)
                pwd_salt = password + salt
                password = pwd_salt.encode('utf-8')
                hashed = bcrypt.hashpw(password, bcrypt.gensalt(16))
                hashed = hashed.decode()
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
    INSERT INTO accounts (account_id, username, password, salt) 
    VALUES ("{new_max_id}", "{username}", "{hashed}", "{salt}");""")

                mydb.commit()

            elif len(password) <= 5:
                print("Password is too short")
                create_account()
            elif len(password) >= 20:
                print("Password is too large")
                create_account()
        else:
            print("username already exists. Try another \n")
            create_account()
    else:
        print("Invalid username length. Try again")


def store_password():
    username = input("""Username
    >""").lower()
    if len(username) > 20 or len(username) < 2:
        return print("invalid password length")
    mycursor.execute(f"""SELECT * FROM accounts WHERE username = '{username}' """)
    myresult = mycursor.fetchone()
    if not myresult:
        return print("Failure")
    hashed = myresult[2]
    salt = myresult[3]
    hashed_password = hashed.encode('utf-8')
    password = input("""Password
    >""")
    password = password + salt
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        account_id = myresult[0]
        location = input("""Website name
    >""").lower()
        mycursor.execute(f"""
SELECT username FROM stored_passwords WHERE location = '{location}' 
and username = '{username}'""")
        myresult = mycursor.fetchone()
        # in order to see if that username already exists in the database
        if not myresult:
            sub_username = input("""What is your username for that website?
        >""")
            the_password = input("""What is your password for that website?
        >""")
            notes = input("""Any personal notes? Such as the website link?
        >""")
            notes_encrypt = aes_encrypt(password.encode(), notes.encode())
            notes_encrypt_x2 = aes_encrypt(password.encode(), notes_encrypt.encode())

            def get_random_string(length):
                # Random string with the combination of lower and upper case
                letters = string.ascii_letters
                result_str = ''.join(random.choice(letters) for i in range(length))
                return result_str
            salt_letter = get_random_string(12)
            salt_number = random.randint(99999999999, 999999999999)
            salt = salt_letter + str(salt_number)
            pwd_salt = the_password + salt
            encrypted_pwd = aes_encrypt(password.encode(), pwd_salt.encode())
            encrypted_pwd_x2 = aes_encrypt(password.encode(), encrypted_pwd.encode())
            if account_id != "" and location != "" and sub_username != "" and the_password != "":
                mycursor.execute(f""" 
    INSERT INTO stored_passwords (account_id, username, location, website_username, the_password, salt, notes) 
    VALUES ("{account_id}", "{username}", "{location}", "{sub_username}", "{encrypted_pwd_x2}", "{salt}",
"{notes_encrypt_x2}")""")
                mydb.commit()
            else:
                print("failure")
        else:
            print("That website name already exists")
    else:
        print("failure")


def read_password():
    username = input("""Username
    >""").lower()
    mycursor.execute(f"""SELECT * FROM accounts WHERE username = '{username}' """)
    myresult = mycursor.fetchone()
    if not myresult:
        return print("Failure")
    hashed = myresult[2]
    salt = myresult[3]
    hashed_password = hashed.encode('utf-8')
    password = input("""Password
    >""")
    password = password + salt
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        account_id = myresult[0]
        location = input("""Website name
    >""").lower()
        mycursor.execute(f"""
SELECT * FROM stored_passwords WHERE username = '{username}' AND location = '{location}';
""")
        myresult = mycursor.fetchone()
        decrypt_web_pwd = aes_decrypt(password.encode(), (myresult[4]))
        decrypt_web_pwd_x2 = aes_decrypt(password.encode(), decrypt_web_pwd)
        salt = myresult[5]
        web_pwd_no_salt = decrypt_web_pwd_x2.replace(salt, "")
        decrypt_notes = aes_decrypt(password.encode(), myresult[6])
        decrypt_notes_x2 = aes_decrypt(password.encode(), decrypt_notes)
        print(f"""
Website Name: {myresult[2]}
Website Username: {myresult[3]}
Website Password: {web_pwd_no_salt}
Notes: {decrypt_notes_x2}
""")
    else:
        print("Failure")


request = input("""
Commands
    - "Create" : Create a master account. That password is used to encrypt
    and decrypt passwords for websites. 
    - "Store" : Save website credentials in database
    - "Read" : View credentials for website
>""").lower()

if __name__ == '__main__':
    if request == "create":
        create_account()
        mydb.close()
    elif request == "store":
        store_password()
        mydb.close()
    elif request == "read":
        read_password()
        mydb.close()
    else:
        print("failure")
        mydb.close()
