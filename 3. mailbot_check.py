# MAil_Bot_Test  
""" Please not that this program is just the extended test of the main program (i.e, ToDo_ist.app.py). It is also to be noted that many of the part of this program may
may not be integrated same on the code because this test was just to get connection of the Todoist09 account as default sender."""
import os
import smtplib
from email.message import EmailMessage

# Set the email login credentials as environment variables
email_user = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASSWORD')

# Create the email message
msg = EmailMessage()
msg['Subject'] = ''
msg['From'] = email_user
msg['To'] = input("Enter receiver email address: ")
msg.set_content('The important thing is that code runs :))))))')

# Set up the SMTP server
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
    smtp_server.login(email_user, email_password)
    smtp_server.send_message(msg)
