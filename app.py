from flask import Flask, request, render_template
from celery import Celery
import smtplib
from email.mime.text import MIMEText
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Initialize Flask web application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure RabbitMQ and Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Retrieve email credentials and log file path from environment variables
mail = os.getenv('EMAIL')
password = os.getenv('APP_PASSWORD')
log_path= os.getenv('PATH_TO_LOGS')

# Check if the log file path already exists; if not, create an empty log file
if not os.path.exists(log_path):
    with open(log_path, 'w') as log_file:
        log_file.write('')

# Define a Celery task to send an email asynchronously
@celery.task
def send_email(to_email):
    sender = mail
    msg = MIMEText("This is a test email sent from the messaging system.")
    msg['Subject'] = "Test Email"
    msg['From'] = sender
    msg['To'] = to_email  # Assign the 'To' field correctly
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except Exception as e:
        # Log any errors encountered during email sending
        logging.error(f"Failed to send email to {to_email}: {str(e)}")

# Define the root route handler for the Flask app
@app.route('/', methods=['GET', 'POST'])
def index(sendmail=None, talktome=False):
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    # If the 'sendmail' parameter is present, queue an email to be sent
    if sendmail:
        send_email.delay(sendmail)
        return f"Email queued to be sent to {sendmail}"
    
    # If the 'talktome' parameter is present, append the current timestamp to the log file
    if talktome:
        with open(log_path, 'a') as log_file:
            log_file.write(f"{datetime.now()}\n")
        return f"Logged current time to {log_path}"
    
    return render_template('welcome.html', sendmail=sendmail, talktome=talktome)

# Define a route to display the contents of the log file
@app.route('/logs')
def view_logs():
    try:
        # Read and display the contents of the log file
        with open(log_path, 'r') as log_file:
            log_content = log_file.read()
        return f"<pre>{log_content}</pre>"  # Display logs in preformatted text
    except FileNotFoundError:
        # Handle case where the log file does not exist
        return "Log file not found."

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)