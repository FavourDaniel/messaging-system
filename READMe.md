# Messaging System with RabbitMQ/Celery and Python Application behind Nginx

This deploys a Python application behind Nginx that interacts with RabbitMQ/Celery for email sending and logging functionality. The below architecture diagram visualizes the process:
![app-architecture](https://github.com/user-attachments/assets/7c964cc8-27ed-47b0-9119-cde2c41d5ec8)


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

<img width="1675" alt="Screenshot 2024-07-12 at 20 29 55" src="https://github.com/user-attachments/assets/a4c5a5c3-a2b1-4e02-8d9b-a5613829a77d">


The default login credential for both the username and password is "guest".


## Set up Celery

Celery is an asynchronous task queue/job queue system for Python, designed to handle real-time operations. It can be used to schedule tasks that run in the background, allowing for concurrency and parallel execution of code.

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


### Email setup
You can use an existing email address or create a new one. Configure 2FA for whichever.
In the email settings, search "App Password" and create an App password. Be sure to copy the password somewhere.

<img width="1040" alt="Screenshot 2024-07-13 at 08 01 24" src="https://github.com/user-attachments/assets/d75fc657-ccb6-47af-9767-0932bfa7afb0">

<img width="1333" alt="Screenshot 2024-07-13 at 08 02 16" src="https://github.com/user-attachments/assets/cc4ca3f5-e095-450b-b55c-4a7e34b93d12">

A `.env.template` file has been provided in this repo. Change the name to `.env` and replace the email and app password env variables.

## Set Up Log Directory
The time logs should be logged at `/var/log/messaging_system.log`. This path has already been set in the app to be created if it doesn't exist but you can configure it manually using the below commands:
```
sudo touch /var/log/messaging_system.log
sudo chmod a+rw /var/log/messaging_system.log
```
The code has already been written to do this, but you can run these commands if you want a manual approach.

### Install Nginx
Install Nginx on your local and replace the default `nginx.conf` file with the one provided in this repo. This allows Nginx to route requests from localhost:5000 where the flask app will be running.

### Start the Application
- In your terminal, run:
```
python app.py  --port 5000
```

- In another terminal, run:
```
celery -A app.celery worker --loglevel=info
```

- Access the app at `localhost`
<img width="1680" alt="Screenshot 2024-07-13 at 13 45 51" src="https://github.com/user-attachments/assets/0c93e172-ec4c-4e52-8b72-ceb05ffcbd77">

  
- In another tab, load `http://localhost:5000/?talktome=true` to generate time logs

<img width="736" alt="Screenshot 2024-07-12 at 21 55 28" src="https://github.com/user-attachments/assets/1775c5fe-00d5-485d-83a2-64d5dee0f8c1">

- In another tab, load `http://localhost:5000/?sendmail=kuberneteslinux@gmail.com`
<img width="737" alt="Screenshot 2024-07-12 at 21 56 22" src="https://github.com/user-attachments/assets/93da44a2-cd1e-4065-9b4c-a1d6730f79e7">

- Check RabbitMQ to be sure it was queued successfully
<img width="1680" alt="Screenshot 2024-07-13 at 13 56 38" src="https://github.com/user-attachments/assets/149662c3-822e-4680-b3aa-11d74ceb93ec">

After some seconds, it should change to ready
<img width="1680" alt="Screenshot 2024-07-13 at 13 56 47" src="https://github.com/user-attachments/assets/906b8595-20ac-46aa-bade-9aaa0e52b5c6">

If you check the terminal where Celery is running, you should see the below:

<img width="1334" alt="Screenshot 2024-07-12 at 21 58 24" src="https://github.com/user-attachments/assets/b06898ae-36c0-4263-b07e-b3f839ba4a6a">

This indicates that the email-sending task was received, processed by a specific Celery worker (ForkPoolWorker-8), and completed successfully.

- Check your email address for the mail sent

<img width="1402" alt="Screenshot 2024-07-12 at 22 04 06" src="https://github.com/user-attachments/assets/174edfe6-db12-4d2d-8f21-7a7733d8fafc">

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

You can create a free one on your ngrok dashboard under the setup and installation tab.

<img width="948" alt="Screenshot 2024-07-12 at 21 52 40" src="https://github.com/user-attachments/assets/7d19b1cf-f354-4de9-9e5b-9d2ea2c511c7">

Copy and paste command displayed
```
ngrok http --domain=<unique-domain.ngrok-free.app> 80
```
<img width="1440" alt="Screenshot 2024-07-12 at 21 47 32" src="https://github.com/user-attachments/assets/81d108e6-fb6f-4833-8319-bb930b714935">

- Copy and open the URL in your browser
<img width="1677" alt="Screenshot 2024-07-12 at 20 54 12" src="https://github.com/user-attachments/assets/64a1215e-fe10-4f80-b41e-1b189fbd5fed">

- Click on the `Visit Site` button to access your website
<img width="1680" alt="Screenshot 2024-07-13 at 13 45 28" src="https://github.com/user-attachments/assets/32b0cadc-6112-4cbf-a6bf-be60b33dab57">

- Access the time logs using the url
<img width="1012" alt="Screenshot 2024-07-13 at 13 50 16" src="https://github.com/user-attachments/assets/f4977c87-5693-4cd4-a90d-f8b207dff98a">

- Send an email
<img width="1012" alt="Screenshot 2024-07-13 at 13 50 40" src="https://github.com/user-attachments/assets/5bc8f8cf-d634-4693-b3cc-ce00ba4436b1">

- You can also access your Ngrok dashboard at `localhost:4040`
<img width="1680" alt="Screenshot 2024-07-13 at 13 52 13" src="https://github.com/user-attachments/assets/6a753170-773a-4acc-b145-1b1987339d27">

