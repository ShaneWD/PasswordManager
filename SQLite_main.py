import sqlite3
import random
import string
import bcrypt


mydb = sqlite3.connect('SQLite_PWD.db')

mycursor = mydb.cursor()
'''
mycursor.execute("""CREATE TABLE accounts (
        account_id INT NOT NULL UNIQUE PRIMARY key,
        username TEXT NOT NULL,
        password TEXT NOT NULL
                )""")
'''

# mycursor.execute("INSERT INTO accounts VALUES ('1', 'delete', 'delete' )")
# mycursor.execute("SELECT * FROM ACCOUNTS")
# data = mycursor.fetchall()

# mydb.commit()


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


