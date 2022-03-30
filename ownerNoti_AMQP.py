#from crypt import methods
import code
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
    "apiKey": "AIzaSyARQ8P2pOqIaSxca0QL_H5ItCMgaS4g1pA",
    "authDomain": "ownernotificationmicroservice.firebaseapp.com",
    "databaseURL": "https://ownernotificationmicroservice-default-rtdb.asia-southeast1.firebasedatabase.app",    
    "projectId": "ownernotificationmicroservice",
    "storageBucket": "ownernotificationmicroservice.appspot.com",
    "messagingSenderId": "904826677540",
    "appId": "1:904826677540:web:ce6364b2b581541c39ebb1"
}

firebase = pb.initialize_app(firebaseConfig)
db = firebase.database() #user realtime db

monitorBindingKey='ownerNotification'

def receiveOwnerNotification():
    direct_amqp_setup.check_setup()
        
    queue_name = 'Owner_Notification'
    
    # set up a consumer and start to wait for coming messages
    direct_amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    direct_amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a notification by " + __file__)
    processNotification(body)
    # processNotification(json.loads(body))

    print() # print a new line feed

# ownernoti  {'UID': 'mouse', 'JID': '-MzPxkCGomRlRCTllVil', 'CID': '988'}
def processNotification(data):
    data = json.loads(data)
    print(data)
    print(type(data))

    if type(data) == str:
        data2 = json.loads(data)
        print(data2)
        print(type(data2))
        CID = data2['CID']
        data2["posted_timestamp"] = str(datetime.now()) 
        db.child(CID).push(data2)
    else:
    # print(data['CID'])
        CID = data['CID']
        data["posted_timestamp"] = str(datetime.now()) 
        db.child(CID).push(data)

    # for key in data:
    #     if key == 'data':
    #         result = json.loads(data["data"])
    #         result["posted_timestamp"] = str(datetime.now()) 
    #         db.child(result["CID"]).push(result)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, direct_amqp_setup.exchangename))
    receiveOwnerNotification()