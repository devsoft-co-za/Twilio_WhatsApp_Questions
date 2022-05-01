# Smart Wage WhatsApp Questions 

### Setup:
##### Pre-requisite: Free Twiolio WhatsApp Sandbox set up 
1. clone this repository
2. setup venv `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`
3. Ngrok (for local web hook receiving)
4. SQLite db setup:
`sqlite3 interactions.db`
`CREATE TABLE messages(cell INT, message TEXT)`
CTRL+D to exit


### Deployment: 
Using Ubuntu Server 20.04 with Nginx, uwsgi and systemd. 
##### Nginx config file: 
```
server {
    listen 80;
    server_name chatbot.devsoft.co.za;

    location / {
                include uwsgi_params;
                uwsgi_pass unix:/home/tom/Twilio_WhatsApp_Questions/whatsapp_questions.sock;
        }

}
```
##### Systemd unit file: 

```
[Unit]
Description=uWSGI instance to serve whatsapp_questions
After=network.target

[Service]
User=tom
Group=www-data
WorkingDirectory=/home/tom/Twilio_WhatsApp_Questions
Environment="PATH=/home/tom/Twilio_WhatsApp_Questions/venv/bin"
ExecStart=/home/tom/Twilio_WhatsApp_Questions/venv/bin/uwsgi --ini whatsapp_questions.ini

[Install]
WantedBy=multi-user.target
```

### Usage: 

#### Run Locally: 
Using Ngrok https://dashboard.ngrok.com/get-started/setup

`./ngrok http http://127.0.0.1:5000`

Copy the ngrok url, insert into Twilio Sandbox Configuration ("When a message comes in") link 


Run the Flask application:
`export FLASK_ENV=development`
`python app.py`

Send a WhatsApp message to your Twilio sandbox number

Check the resulting database using the api: 

`curl --location --request GET '127.0.0.1:5000/get_messages'`


#### Check the deployed api: 
`curl --location --request GET 'http://chatbot.devsoft.co.za/get_messages'` *still todo

