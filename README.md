 ## Create SQL Database 
 ###### I used MySQL Workbench 
 Create databse titled "pwd_manager". 
 Two tables needed; 
 - ## accounts
 ```sql
 CREATE TABLE `accounts` (
  `account_id` int NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `the_password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
 ```
 - ## stored_passwords
```sql
CREATE TABLE `stored_passwords` (
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `the_password` varbinary(1000) DEFAULT NULL,
  `account_id` int NOT NULL,
  `notes` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `salt` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `website_username` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  KEY `account_id` (`account_id`),
  CONSTRAINT `stored_passwords_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
###### It is also reccomnded that for *stored_passwords* you type;
```sql 
ALTER TABLE stored_passwords CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
