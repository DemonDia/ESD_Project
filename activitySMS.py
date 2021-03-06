#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script


# receive http status code that are not 400

import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import pyrebase as pb
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

import json
import os

import topic_amqp_setup

firebaseConfig = {
  "apiKey": "AIzaSyAJyo8v_ol6NZwDkYzj9R7-tIn2q8IyiP4",
  "authDomain": "activitymicroservice.firebaseapp.com",
  "databaseURL": "https://activitymicroservice-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "activitymicroservice",
  "storageBucket": "activitymicroservice.appspot.com",
  "messagingSenderId": "230760775714",
  "appId": "1:230760775714:web:9ef96d00b609383d1f8a7b"
}

firebase = pb.initialize_app(firebaseConfig)
db = firebase.database() #user realtime db

monitorBindingKey='#'

def receiveLog():
    topic_amqp_setup.check_setup()
        
    queue_name = 'Activity_Log'
    
    # set up a consumer and start to wait for coming messages
    topic_amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    topic_amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log by " + __file__)
    processLog(json.loads(body))
    print() # print a new line feed


def processLog(data):
    # data = json.loads(data)
    print("Recording a log:")

    if type(data) == str:
        data2 = json.loads(data)
        print(data2)
        print(type(data2))
        data2["posted_timestamp"] = str(datetime.now()) 
        db.child("activities").push(data2)
    else:
        data["posted_timestamp"] = str(datetime.now()) 
        db.child("activities").push(data)

    # data["posted_timestamp"] = str(datetime.now()) 
    # db.child("activities").push(data)


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, topic_amqp_setup.exchangename))
    receiveLog()

