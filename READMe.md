# Messaging System with RabbitMQ/Celery and Python Application behind Nginx

This deploys a Python application behind Nginx that interacts with RabbitMQ/Celery for email sending and logging functionality.

## Set up RabbitMQ Locally

- Install RabbitMQ:
```
brew install rabbitmq ##for macOS users
```
- Start RabbitMQ:
```
# starts a local RabbitMQ node
brew services start rabbitmq
```
- Access RabbitMQ on http://localhost:15672/
==insert image

The default login credential for both the username and password is "guest".


## Set up Celery

Celery is a ....so it needs to be installed with Python's package manager. This will be done in a virtual environment.

- Create and activate a Python virtual environment
```
python3 -m venv myenv
source myenv/bin/activate
```

- Install Celery and other requirements from the requirements.txt file
```
pip install -r requirements.txt
```

## Setup and Start the Python application
The provided Python application creates a simple web application that does two things:

1. Sends Emails: It allows you to trigger the sending of an email by visiting a specific URL in your web browser. The email sending itself happens in the background through Celery. Celery is configured to use RabbitMQ as its message broker (where it keeps track of tasks). It creates an email message, connects to a Gmail SMTP server, logs in, and sends the email.

2. Logs Time: It also has a feature to log the current time to a file when you visit another specific URL.


### Email
You can choose to use an existing email address or create a new one. Configure 2FA for whichever.
In the email settings, search "App Password" and create an App password. Be sure to copy the password somewhere.

A `.env.example` file has been provided in this repo. Change the name to `.env` and replace the email and app password env variables.

## Set Up Log Directory
The time logs should be logged at `/var/log/messaging_system.log`.

Create and grant permission to the file:
```
sudo touch /var/log/messaging_system.log
sudo chmod a+rw /var/log/messaging_system.log
```

### Start the Application
In your terminal, run:
```
python app.py  --port 5000
```

In another terminal, run:
```
celery -A app.celery worker --loglevel=info
```

Access the app at `localhost:5000`
In another tab, load `http://localhost:5000/?talktome=true` to generate time logs
In another tab, load `http://localhost:5000/?sendmail=kuberneteslinux@gmail.com`

## Setup Ngrok

