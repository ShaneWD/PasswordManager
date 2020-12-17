# pip install mysql-connector-python
# pip install bcrypt


import bcrypt
import mysql.connector
import random
import string

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

                salt_letter = get_random_string(8)
                salt_number = random.randint(9999, 99999)
                salt = "salt" + salt_letter + str(salt_number)
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
    INSERT INTO accounts (account_id, username, the_password, salt) 
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
        create_account()


def store_password():
    username = input("""Username
    >""")
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
    >""")
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
            notes = input("""Any personal notes (DO NOT include confidential information) """)

            def get_random_string(length):
                # Random string with the combination of lower and upper case
                letters = string.ascii_letters
                result_str = ''.join(random.choice(letters) for i in range(length))
                return result_str
            salt_letter = get_random_string(8)
            salt_number = random.randint(9999, 99999)
            salt = "salt" + salt_letter + str(salt_number)
            pwd_salt = the_password + salt
            # To add a random set of characters at the end of the plain-text password before encryption.
            # This is because two identical passwords will result in the same encrypted text. Thus, salt is needed.
            # For decryption,the program looks at the row salt and removes those characters after decryption.
            '''
            ex: 
            Password = pwd123
            A salt is generated and added to the password, as well as its own separate column. 
            Before encryption, it looks is updated to (similar to): pwd123saltHnaH18723
            Then it is encrypted 
            After decryption, it looks like: pwd123saltHnaH18723
            The program looks at the dedicated salt column, and removes it from the plain text after decryption. 
            '''
            if account_id != "" and location != "" and sub_username != "" and the_password != "":
                mycursor.execute(f""" 
    INSERT INTO stored_passwords (account_id, location, notes, the_password, username, salt, website_username) 
    VALUES ("{account_id}", "{location}", "{notes}", aes_encrypt("{pwd_salt}", "{password}"), "{username}", "{salt}",
    "{sub_username}");""")
                mydb.commit()
            else:
                print("failure")
        else:
            print("That website name already exists")
    else:
        print("failure")


def read_password():
    username = input("""Username
    >""")
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
    >""")
        mycursor.execute(f"""
SELECT *, REPLACE(CAST(AES_DECRYPT(the_password,'{password}') as char(10000)), salt, ""), salt
FROM stored_passwords WHERE username = '{username}' AND location = '{location}';
""")
        # the "REPLACE" command is the code responsible for removing the salt fom the plain-text password
        myresult = mycursor.fetchone()
        print(f"""
Website Name: {myresult[0]}
Website Username: {myresult[6]}
Website Password: {myresult[7]}
Notes: {myresult[3]}
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
if request == "create":
    create_account()
elif request == "store":
    store_password()
elif request == "read":
    read_password()
else:
    print("failure")


