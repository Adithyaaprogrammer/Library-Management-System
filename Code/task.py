from celery import shared_task
from time import sleep
import flask_excel as excel
from models import *
from mail import send_email
from flask import render_template_string

@shared_task
def add(x, y):
    sleep(30)
    return x + y

import csv
from io import StringIO

@shared_task(ignore_result=False)
def create_csv():
    user_action = UserBook.query.with_entities(
        UserBook.user_id, UserBook.book_id, UserBook.issue, UserBook.return_date
    ).all()
    
    # Create a CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write the header
    writer.writerow(['user_id', 'book_id', 'issue', 'return_date'])
    
    # Write the data rows
    for action in user_action:
        writer.writerow([
            action.user_id, action.book_id, action.issue, action.return_date or ''
        ])
    
    # Move to the beginning of the StringIO buffer
    output.seek(0)
    
    # Write the CSV data to a file
    with open('./user_downloads/user_action.csv', 'w', newline='') as f:
        f.write(output.getvalue())
    
    return 'user_action.csv'

@shared_task(ignore_result = True)
def daily_reminder():
    status = 'approve'
    user_approve = UserBook.query.filter_by(status=status).all()
    for i in user_approve:    
        user = User.query.filter_by(id=i.user_id).first()
        book = Book.query.filter_by(id=i.book_id).first()
        time_left = (i.due - datetime.now()).days  # Get the number of days left
        
        # Generate the HTML email content
        email_html_content = render_template_string('''
        <html>
        <body>
            <h2>Dear {{ user_name }},</h2>
            <p>This is a reminder to return the book <strong>{{ book_title }}</strong> that you borrowed.</p>
            <p>You have <strong>{{ time_left }} days</strong> left to return the book.</p>
            <p>Please make sure to return it on time to avoid any late fees.</p>
            <br>
            <p>Best regards,</p>
            <p>The Library Team</p>
        </body>
        </html>
        ''', user_name=user.name, book_title=book.name, time_left=time_left)
        
        # Call the daily reminder task for each user
        send_email(user.email, "Return Reminder", email_html_content)
    return 'Email_sent'
