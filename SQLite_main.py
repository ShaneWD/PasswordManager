import sqlite3

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
mycursor.execute("SELECT * FROM ACCOUNTS")
data = mycursor.fetchall()
for row in data:
    print(row)
# mydb.commit()


