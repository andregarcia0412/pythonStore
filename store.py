import pyodbc
import bcrypt
from datetime import datetime, date, timedelta

def command_to_database(command: str):
    connection.cursor().execute(command)
    connection.cursor().commit()

def read_table(command: str):
    cursor.execute(command)
    for row in cursor.fetchall():
        print(row)

def encrypt_password(senha):
    salt = bcrypt.gensalt()
    password_bytes = senha.encode()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash

def verify_password(password_input, hash):
    if bcrypt.checkpw(password_input.encode(), hash):
        return True
    else:
        return False

def user_create_account():
    user = str(input("Create your username\n")).strip()
    email = str(input("Type your email\n")).strip()
    password = str(input("Create your password\n")).strip()
    password = encrypt_password(password).decode()
    return user, email, password

def user_login():
    email = str(input("Type your email\n")).strip()
    password = str(input("Type your password\n")).strip()
    return email,password

def select_all(table):
    cursor.execute(f"""SELECT * FROM {table}""")
    for row in cursor.fetchall():
        print(row)

def create_announcement(username):
    product_name = input("What's the name of the product you want to sell?\n").strip()
    price = input("How much is it?\n").strip()
    cursor.execute("""INSERT INTO sale_announcements(product_name, price, user_email) VALUES(?, ?, ?)""", (product_name, price, username))
    cursor.commit()

def buy_product(user_email):
    product_id = input("What's the ID of the product you want to buy?\n").strip()
    cursor.execute("""SELECT price FROM sale_announcements WHERE sale_id = ?""",(product_id,))
    row_price = cursor.fetchone()
    item_price = row_price[0]
    cursor.execute("""SELECT product_name FROM sale_announcements WHERE sale_id = ?""",(product_id,))
    row_name = cursor.fetchone()
    item_name = row_name[0]
    
    confirmation = input(f"The item {item_name} has a price of {item_price}, do you confirm you want to buy it?\n1. Yes\n2. No\n")
    if confirmation == "1":
        cursor.execute("""INSERT INTO shopping_history (user_email, product_name, sale_date, price) VALUES(?, ?, ?, ?)""", (user_email, item_name, str(date.today()), item_price))
        cursor.commit()
        cursor.execute("""DELETE FROM sale_announcements WHERE sale_id = ?""", (product_id,))
        cursor.commit()
        print("Purchase done sucessfully")
    else:
        return False    

def get_username(user_email):
    cursor.execute("""SELECT username FROM Login WHERE email = ?""", (user_email,))
    username = cursor.fetchone()[0]
    return username

def see_shopping_history(user_email):
    cursor.execute("""SELECT product_name FROM shopping_history WHERE user_email = ?""",(user_email))
    return cursor.fetchall()

def verify_empty_table(table):
    cursor.execute(f"""SELECT * FROM sale_announcements""")
    count = cursor.fetchone()
    if count == None:
        return True
    else:
        return False
    
def verify_existing_user(table, user_email):
    cursor.execute(f"""SELECT username FROM Login WHERE email = ?""",(user_email, ))
    count = cursor.fetchone()
    if count == None:
        return False
    else:
        return True
    
def main_screen():
    logged_choice = input("1. Sell product\n2. Buy product\n3. See all offers\n4. Shopping history\n5. Cancel\n")
    if logged_choice == "1":
        create_announcement(get_username(user_email))
        print("Your product was succesfully announced")
        return_to_main = input("Type 1 to return\n")
        if return_to_main == "1":
            main_screen()
    elif logged_choice == "2":
        buy_product(user_email)
        return_to_main = input("Type 1 to return\n")
        if return_to_main == "1":
            main_screen()
    elif logged_choice == "3":
        if verify_empty_table('sale_announcements'):
            print("There are no items for sale")
            return_to_main = input("Type 1 to return\n")
            if return_to_main == "1":
                main_screen()
        else:
            select_all('sale_announcements')
            return_to_main = input("Type 1 to return\n")
            if return_to_main == "1":
                main_screen()
            else:
                print("Come back later!")
    elif logged_choice == "4":
        if see_shopping_history(user_email) == []:
            print("No items in history")
            return_to_main = input("Type 1 to return\n")
            if return_to_main == "1":
                main_screen()
        else:
            print(see_shopping_history(user_email))
            return_to_main = input("Type 1 to return\n")
            if return_to_main == "1":
                main_screen()
    elif logged_choice == "5":
        print("Come back later!")
        return
    else:
        print("Invalid option")
        main_screen()

connection_data = (
    "Driver={SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=Store;"
)
connection = pyodbc.connect(connection_data)
cursor = connection.cursor()

print("== Virtual Store ==")
print("== What do you want to do? ==")
choice = input("1. Create account\n2. Log in\n")

if choice == "1":
    username, user_email, user_password = user_create_account()
    if not verify_existing_user('Login', user_email):
        cursor.execute("""INSERT INTO Login(username, email, password)
        VALUES
            (?, ?, ?)""", (username, user_email, user_password))
        cursor.commit()
        print("Account created succesfully")
        main_screen()
    else:
        print("There is an account linked to this email that already exists")

elif choice == "2":
    user_email, user_password = user_login()
    cursor.execute("""SELECT password FROM Login WHERE email = ?""", user_email,)
    row = cursor.fetchone()
    if row == None:
        print("User not found")
    else:
        saved_password = row[0]
        if verify_password(user_password, saved_password.encode()):
            main_screen()
        else:
            print("Incorrect password")
