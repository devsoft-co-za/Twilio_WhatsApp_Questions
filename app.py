from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse

import sqlalchemy as db
import pandas as pd
import json
import os


# function to save interaction to DB
def save_interaction(cell_number, message_content):
    engine = db.create_engine('sqlite:///interactions.db')
    connection = engine.connect()
    metadata = db.MetaData()
    messages = db.Table('messages', metadata,
                        autoload=True, autoload_with=engine)
    statement = messages.insert().values(
        cell=cell_number, message=message_content)
    connection.execute(statement)


# function to collate all messages received - returns a dictionary
def all_messages():
    engine = db.create_engine('sqlite:///interactions.db')
    connection = engine.connect()
    metadata = db.MetaData()
    messages = db.Table('messages', metadata,
                        autoload=True, autoload_with=engine)
    results = connection.execute(db.select([messages])).fetchall()
    df = pd.DataFrame(results)
    df.columns = results[0].keys()
    df.head(2)
    # get results in dictionary format cell: [messages]
    results_formatted = df.groupby(['cell']).apply(
        lambda x: x['message'].tolist()).to_dict()
    # print(results_formatted)
    return(results_formatted)


app = Flask(__name__)


# this is the webhook to handle Twilio http
@app.route("/", methods=['GET', 'POST'])
def whatsapp_reply():
    # Get message content:
    # all_content = request.values
    # print("all content is: ", all_content)
    body = request.values.get('Body', None)

    cell_number = request.values.get('From', None)
    # cell as a number:
    cell_short = cell_number.rsplit("+")[1]  # needs checking
    # print("cell short number: ", cell_short)
    # save cell and message to db:
    save_interaction(cell_short, body)

    # todo: if already had interaction, change the response below?
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message(
        "Thank you for your enquiry. What do you think of this response?")
    # print(str(resp))
    return str(resp)


# api route to get messages grouped by cell number in Json format
@app.route("/get_messages", methods=['GET'])
def get_messages():
    # get dictionary of all interactions:
    results_formatted = all_messages()
    # convert to json for response:
    json_object = json.dumps(results_formatted, indent=4)
    # print(json_object)
    return(json_object)


@app.route("/show_messages")
def show_messages():
    results_formatted = all_messages()
    return render_template("index.html", messages=results_formatted)


if __name__ == "__main__":
    development = os.environ['FLASK_ENV']
    if development == "development":
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0')
