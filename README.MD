# Smart Wage WhatsApp Questions 

### Setup:
##### Pre-requisite: Free Twiolio WhatsApp Sandbox set up 
1. clone this repository
2. cd repository folder
3. setup venv `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`
4. Install Ngrok (for local web hook receiving)
5. SQLite db setup: *-interactions.db already included, setup for reference*
`sqlite3 interactions.db`
`CREATE TABLE messages(cell INT, message TEXT);`
CTRL+D to exit

### Usage: 

#### Run this locally (instructions are for Linux): 
Using Ngrok https://dashboard.ngrok.com/get-started/setup

ngrok binary needs to be installed
`./ngrok http http://127.0.0.1:5000`

Copy the ngrok url shown in the terminal and insert into Twilio Sandbox Configuration ("When a message comes in") link box. 

Run the Flask application:
`source venv/bin/activate`
`export FLASK_ENV=development`
`python3 app.py`

Send a WhatsApp message to your Twilio sandbox number

Check the resulting database entry using the api: 

`curl --location --request GET '127.0.0.1:5000/get_messages'`


#### Check the already deployed api: 
`curl --location --request GET 'http://chatbot.devsoft.co.za/get_messages'` 

### Deployment: 
Using Ubuntu Server 20.04 with Nginx, uwsgi and systemd. 

Hosted on DigitalOcean - for full setup instructions see https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
##### Nginx config file: 
```
server {
    listen 80;
    server_name <url or ip of server>;

    location / {
                include uwsgi_params;
                uwsgi_pass unix:/path/to/Twilio_WhatsApp_Questions/whatsapp_questions.sock;
        }

}
```
##### Systemd unit file: 

```
[Unit]
Description=uWSGI instance to serve whatsapp_questions
After=network.target

[Service]
User=username
Group=www-data
WorkingDirectory=/path/to/Twilio_WhatsApp_Questions
Environment="PATH=/path/to/Twilio_WhatsApp_Questions/venv/bin"
ExecStart=/path/to/Twilio_WhatsApp_Questions/venv/bin/uwsgi --ini whatsapp_questions.ini

[Install]
WantedBy=multi-user.target
```



## Not yet implemented - TODO: 
Since this is a demonstration project with a time limit there is much still to do, for example
1. Security. The /get_messages end point and Twilio connection are not secured
2. UI. The /get_messages Json response lacks an interface for viewing outside of the command line 
3. More complex chat. Custom responses depending on the message received, and stage of the conversation. 
4. Proper database integration eg. MySql (already using sqlalchemy though - it's easy to switch)
5. Easy deployment path (docker, git hooks, other eg Google Cloud Platform..)
6. Customers table for the db 
7. Full Twilio service (outside of the free Sandbox)