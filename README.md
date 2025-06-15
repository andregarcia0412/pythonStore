# pythonStore
Store app made in python with SQL Server and pyodbc to handle the database, bcrypt to encrypt the passwords and datetime to get the current date;

To run it you need to create a database named "Store" with 3 tables:

Login(username varchar(50), email PRIMARY KEY varchar(50), password varchar(255));

sale_announcements(sale_id int IDENTITY (1,1) PRIMARY KEY, product_name varchar(60), price decimal(10,2), user_email varchar(50));

shopping_history(history_id int IDENTITY(1,1) PRIMARY KEY, user_email varchar(50), product_name varchar(50), sale_date date, price decimal(10,2));

##
