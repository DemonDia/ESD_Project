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

@app.route("/ownerNotification/<string:CID>")
def get_owner_noti(CID):
    try:
        jobApp = db.child(CID).get()
        print('this is jobApp', jobApp)
        jobAppDict = {}    

        for app in jobApp.each():
            jobAppDict[app.key()] = app.val()
        
        return jsonify(
            {
                "code": 201,
                "data": json.dumps(jobAppDict)
            }
            ), 201
    
    except Exception as e:
        print("OMG")
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while finding the jobs. " + str(e)
            }
        ), 500

# @app.route("/ownerNotification/<string:CID>", methods = ["POST"])
# def post_noti(CID):
#     try:
#         data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
#         data = json.loads(data)
#         print(data)
#         data["posted_timestamp"] = str(datetime.now())
#         db.child(CID).push(data)

#         return jsonify(
#             {
#                 "code": 201,
#                 "data": data
#             }
#             ), 201

#     except Exception as e:
#         print(e)

#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred while posting the user's notification. " + str(e)
#             }
#         ), 500


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    app.run(port = 5010,debug = True)
