#from crypt import methods
from importlib.metadata import requires
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pyrebase as pb
import json

import direct_amqp_setup

app = Flask(__name__)
CORS(app)
# sqlalchemy

firebaseConfig = {
    "apiKey": "AIzaSyDBk5Wd0fQBoADxAqOHc39VmVvW9t6Xrts",
    "authDomain": "usernotificationmicroservice.firebaseapp.com",
    "projectId": "usernotificationmicroservice",
    "databaseURL": "https://usernotificationmicroservice-default-rtdb.asia-southeast1.firebasedatabase.app",    
    "storageBucket": "usernotificationmicroservice.appspot.com",
    "messagingSenderId": "91494900010",
    "appId": "1:91494900010:web:3175580a34bdf9b7aefe53" 
}

firebase = pb.initialize_app(firebaseConfig)
db = firebase.database() #user realtime db

monitorBindingKey='userNotification'

def receiveUserNotification():
    direct_amqp_setup.check_setup()
        
    queue_name = 'User_Notification'
    
    # set up a consumer and start to wait for coming messages
    direct_amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    direct_amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a notification by " + __file__)
    processNotification(json.loads(body))
    print() # print a new line feed


def processNotification(data):
    # print(data['app_status'])
    print(data)

    if type(data) == str:
        data2 = json.loads(data)
        print(data2)
        print(type(data2))
        fullname = data2['first'] + data2['last']
        data2["posted_timestamp"] = str(datetime.now()) 
        db.child(fullname).push(data2)
    else:
    # print(data['CID'])
        print('this is the user, ', data)
        fullname = data['first'] + data['last']
        data["posted_timestamp"] = str(datetime.now()) 
        db.child(fullname).push(data)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, direct_amqp_setup.exchangename))
    receiveUserNotification()