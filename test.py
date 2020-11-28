import mysql.connector

f = open("pwd.txt", "r")
pwd = (f.read())
f.close()
mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password=pwd,
                               database='messaging_333')

mycursor = mydb.cursor()

mycursor.execute("""
INSERT INTO message (message_id, account_id, message, username)
VALUES ("1007", "1001", "oh really321?", "Shane");""")

mydb.commit()
