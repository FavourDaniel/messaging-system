from flask import Flask, request
from celery import Celery
import smtplib
from email.mime.text import MIMEText
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
# Configure RabbitMQ and Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

mail = os.getenv('EMAIL')
password = os.getenv('APP_PASSWORD')
log_path= os.getenv('PATH_TO_LOGS')

# Task to send email (simulate task)
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
        logging.error(f"Failed to send email to {to_email}: {str(e)}")


@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        send_email.delay(sendmail)
        return f"Email queued to be sent to {sendmail}"
    
    if talktome:
        with open(log_path, 'a') as log_file:
            log_file.write(f"{datetime.now()}\n")
        return f"Logged current time to {log_path}"
    
    return "Use ?sendmail=email@example.com or ?talktome=true"

@app.route('/logs')
def view_logs():
    try:
        with open('/var/log/messaging_system.log', 'r') as log_file:
            log_content = log_file.read()
        return f"<pre>{log_content}</pre>"  # Display logs in preformatted text
    except FileNotFoundError:
        return "Log file not found."

if __name__ == '__main__':
    app.run(debug=True)