# Smart Wage WhatsApp Questions 

### Setup:
##### Pre-requisite: Free Twiolio WhatsApp Sandbox set up 
1. clone this repository
2. setup venv, pip install requirements.txt
3. Ngrok (for local web hook receiving)
4. SQLite db setup:
`sqlite3 interactions.db`
`CREATE TABLE messages(cell INT, message TEXT)`
CTRL+D to exit


###Deployment: 
Using Ubuntu Server 20.04 with Nginx, uwsgi. 


###Usage: 

#### Run Locally: 
Using Ngrok [https://dashboard.ngrok.com/get-started/setup]
`./ngrok http http://127.0.0.1:5000`
Copy the ngrok url, insert into Twilio Sandbox Configuration ("When a message comes in") link 
Run the Flask application:
`python app.py`
Send a WhatsApp message to your Twilio sandbox number
Check the resulting database using the api: 
`curl --location --request GET '127.0.0.1:5000/get_messages'`

#### Check the deployed api: 
`curl --location --request GET 'chatbot.devsoft.co.za/get_messages'` *todo

