import os    # The installation is used in encrypting the defualt sender's Email and Password [in line 10 & 11]
import ssl   # ([Secure Sockets Layer] is used to encrypt the communication between sender's and reciever end)
import smtplib #([simple mail transfer protocol] this module is used to send messages to any onternet machine)
import mysql.connector #(This module is to connect the python code to RDBMS (managment system at the backend) The Backened is provided separately in the Zip file(.sql))
from datetime import datetime, timedelta #The datetime module provides classes for working with date and time as an objects. It helps in altering, manipulation and formatting dates and time
                                         #timedelta module provides a way to represent duration of the time. It allows arithmetic operations."""

# Set up the email server and login credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 465
email_user = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASSWORD')

# Set up the database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='7600288140@Ss',
    database='ToDo_ist'
)
cursor = db.cursor()

user_id = None
user_email = None

# Function to send an email notification
def send_email(to_email, subject, body):
    # Set up a secure SSL connection to the email server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        # Log in to the email server
        server.login(email_user, email_password)

        # Construct the email message
        message = f'Subject: {subject}\n\n{body}'

        # Send the email
        server.sendmail(email_user, to_email, message)

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

# Function to add a new task to the to-do list
def add_task():
    if not user_id:
        print('Please log in to add a task')
        return

    task_description = input('Enter the task description: ')
    due_date = input('Enter the due date (yyyy-mm-dd): ')
    due_time = input('Enter the due time (hh:mm AM/PM): ')

        # Convert the due date and time to a datetime object
    due_datetime = datetime.strptime(f'{due_date} {due_time}', '%Y-%m-%d %I:%M %p')

    # Insert the new task into the database
    sql = 'INSERT INTO tasks (user_id, description, due_datetime) VALUES (%s, %s, %s)'
    val = (user_id, task_description, due_datetime)
    cursor.execute(sql, val)
    db.commit()

    print('Task added successfully')

    # Send an email notification for the new task
    subject = f'New task added: {task_description}'
    body = f"You've added a new task: {task_description}\nDue Date: {due_date}\nDue Time: {due_time}"
    send_email(user_email, subject, body)

# Function to display the current user's tasks
def display_tasks():
    if not user_id:
        print('Please log in to view your tasks')
        return

    # Select the user's tasks from the database
    sql = 'SELECT * FROM tasks WHERE user_id = %s ORDER BY due_datetime'
    val = (user_id,)
    cursor.execute(sql, val)
    tasks = cursor.fetchall()

    # Print the user's tasks
    if tasks:
        print('Your current tasks:')
        for task in tasks:
            task_id, task_user_id, task_description, task_due_datetime, task_completed = task
            task_due_time = task_due_datetime.strftime('%I:%M %p')
            task_due_date = task_due_datetime.strftime('%Y-%m-%d')
            if task_completed:
                print(f' [X] {task_description} - Due {task_due_date} at {task_due_time}')
            else:
                print(f' [ ] {task_description} - Due {task_due_date} at {task_due_time}')
    else:
        print('You have no current tasks')

# Function to mark a task as completed
def complete_task():
    if not user_id:
        print('Please log in to complete a task')
        return

    task_id = input('Enter the task ID of the task you completed: ')

    # Update the task's completion status in the database
    sql = 'UPDATE tasks SET completed = 1 WHERE id = %s AND user_id = %s'
    val = (task_id, user_id)
    cursor.execute(sql, val)
    db.commit()

    # Send an email notification for the completed task
    sql = 'SELECT * FROM tasks WHERE id = %s'
    val = (task_id,)
    cursor.execute(sql, val)
    task = cursor.fetchone()
    task_description = task[2]
    subject = f'Task completed: {task_description}'
    body = f"You've completed the task: {task_description}"
    send_email(user_email, subject, body)

    print('Task completed successfully')

# Main loop
while True:
    print('\n==== To-Do List ====')
    if user_id:
        print(f'Logged in as {user_email}')
        print('1. Log out')
        print('2. Add task')
        print('3. View tasks')
        print('4. Complete task')
        print('0. Exit')
    else:
        print('1. Sign up')
        print('2. Log in')
        print('0. Exit')

    choice = input('Enter your choice: ')

    if choice == '1':
        if user_id:
            logout()
        else:
            signup()
    elif choice == '2':
        if user_id:
            add_task()
        else:
            login()
    elif choice == '3':
        if user_id:
            display_tasks()
        else:
            print('Please log in to view your tasks')
    elif choice == '4':
        if user_id:
            complete_task()
        else:
            print('Please log in to complete a task')
    elif choice == '0':
        break
    else:
        print('Invalid choice')


#________________________________________________________________________________Thank_you_:-)________________________________________________________________________________________

    


