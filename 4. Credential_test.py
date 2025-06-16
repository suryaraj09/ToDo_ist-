#Credential_test
"""Please note that this program is just to understand the concept behind the successful credential run test of the code in the main program (i.e, To_Do_ist.app.py)
and the program lacks a backend store as it was part of the program after which the database was dropped for this test"""
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='7600288140@Ss',
    database='ToDo_ist'
)
cursor = db.cursor()

user_id = None
user_email = None
# Function to create a new account
def signup():
    username = input('Enter a username: ')
    password = input('Enter a password: ')
    email = input('Enter an email: ')

    # Insert the new user into the database
    sql = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)'
    val = (username, password, email)
    cursor.execute(sql, val)
    db.commit()

    print('Account created successfully')

# Function to log in to an existing account
def login():
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    # Check if the username and password match a user in the database
    sql = 'SELECT * FROM users WHERE username = %s AND password = %s'
    val = (username, password)
    cursor.execute(sql, val)
    user = cursor.fetchone()

    if user:
        global user_id, user_email
        user_id = user[0]
        user_email = user[3]
        print('Logged in successfully')
    else:
        print('Invalid username or password')

# Function to delete a user account
def delete_user():
    confirm = input('Are you sure you want to delete your account? (y/n) ')
    if confirm.lower() == 'y':
        # Delete the user from the database
        sql = 'DELETE FROM users WHERE id = %s'
        val = (user_id,)
        cursor.execute(sql, val)
        db.commit()

        print('Account deleted successfully')
        logout()

# Function to log out of the current account
def logout():
    global user_id, user_email
    user_id = None
    user_email = None
    print('Logged out successfully')