#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import pyrebase as pb
import json
app = Flask(__name__)
CORS(app)

import json
import os

import topic_amqp_setup

firebaseConfig = {
    "apiKey": "AIzaSyC6vFvSWpcY6sS8g1nXvWC3Rgo3X_ZwrqY",
    "authDomain": "errormicroservice.firebaseapp.com",
    "databaseURL": "https://errormicroservice-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "errormicroservice",
    "storageBucket": "errormicroservice.appspot.com",
    "messagingSenderId": "356092494930",
    "appId": "1:356092494930:web:22814fccd220402ae00b8b"
}

firebase = pb.initialize_app(firebaseConfig)
db = firebase.database() #user realtime db

monitorBindingKey='*.error'

def receiveError():
    topic_amqp_setup.check_setup()
    
    queue_name = "Error"  

    # set up a consumer and start to wait for coming messages
    topic_amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    topic_amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an error by " + __file__)
    processError(body)
    print() # print a new line feed

def processError(errorMsg):
    print("Printing the error message:")
    try:
        error = json.loads(errorMsg)
        db.child("errors").push(error)
        print("--JSON:", error)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
        db.child("errors").push(e)
    print()


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, topic_amqp_setup.exchangename))
    receiveError()
