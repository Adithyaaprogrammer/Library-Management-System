from celery import shared_task
from time import sleep
import flask_excel as excel
from models import *

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

