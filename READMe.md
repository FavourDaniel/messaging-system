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

Celery is a asynchronous task queue/job queue system for Python, designed to handle real-time operations and can be used to schedule tasks that run in the background, allowing for concurrency and parallel execution of code.

Celery is a Python package so it will be installed with pip. This will be done in a virtual environment.

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
- In your terminal, run:
```
python app.py  --port 5000
```

- In another terminal, run:
```
celery -A app.celery worker --loglevel=info
```

- Access the app at `localhost:5000`
- In another tab, load `http://localhost:5000/?talktome=true` to generate time logs
- In another tab, load `http://localhost:5000/?sendmail=kuberneteslinux@gmail.com`

## Setup Ngrok

- Install ngrok via Homebrew with the following command:
```
brew install ngrok/ngrok/ngrok
```
- Connect your account
Next, connect your ngrok agent to your ngrok account. If you haven't already, sign up for an ngrok account. Copy your ngrok authtoken from your ngrok dashboard.
Run the following command in your terminal to install the authtoken and connect the ngrok agent to your account.

```
ngrok config add-authtoken <TOKEN>
```
- Create a static domain
You can create a free one on your ngrok dashboard
==insert image
Copy and paste command displayed
```
ngrok http --domain=<unique-domain.ngrok-free.app> 80
```
==insert terminal image
- Copy and run the url in your browser
==insert image
- Access the website
==insert image

- You can also acess your ngrok dashboard at localhost://4040
==insert image