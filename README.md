 # Demo
 <image src= "https://github.com/ShaneWD/PasswordManager/blob/master/pwd_Manager(demo-gif).gif">

 ###### Speed in increased to 150%
 ### What the end-result look likes in the database
 <image src = "https://github.com/ShaneWD/PasswordManager/blob/master/pwd_end_result.png" width = 800>
 
 # Steps
 ## Create SQL Database 
 ###### I used MySQL Workbench 
 Create databse titled "pwd_manager". 
 ```sql
 CREATE DATABASE pwd_manager
 ```
 Two tables needed; 
 - ## accounts
 ```sql
CREATE TABLE `accounts` (
  `account_id` int NOT NULL,
  `username` varchar(20) DEFAULT NOT NULL,
  `the_password` varchar(100) DEFAULT NOT NULL,
  `salt` varchar(30) NOT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
 ```
 - ## stored_passwords
```sql
CREATE TABLE `stored_passwords` (
  `location` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `the_password` varbinary(1000) NOT NULL,
  `account_id` int NOT NULL,
  `notes` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `username` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `salt` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `website_username` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  KEY `account_id` (`account_id`),
  CONSTRAINT `stored_passwords_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
###### It is also reccomnded that for *stored_passwords* you type;
```sql 
ALTER TABLE stored_passwords CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
###### utf8mb4 allows for 4 bytes per character, and allows more chacracter types. This is very benefitial for storing hashed passwords. 
## Setting up MySQL connection
```python
pip install mysql-connector-python
```
- Create a seperate file titled *pwd.txt*. In pwd.txt, type the password you use to log in to your MySQL.
- Also, if needed change the following code in main.py to your correct credentials
```python
mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password=pwd,
                               database='pwd_manager')
```
