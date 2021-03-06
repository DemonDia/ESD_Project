#from crypt import methods
from importlib.metadata import requires
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pyrebase as pb
import json

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

# db.create_all()

# {
#    "JID": "-MyVtBZxF7DzNc969y7_", 
#    "UID": "666666"
# }
@app.route("/ownerNotification/<string:CID>")
def get_user_noti(CID):
    try:
        ownerNotif = db.child(CID).get()
        print('this is ownerNotif', ownerNotif)
        ownerNotifDict = {}    

        for notif in ownerNotif.each():
            print(type(notif.key()))
            print("___________") 
            print("key:",notif.key())
            print("value:",notif.val())
            ownerNotifDict[notif.key()] = notif.val()

        print("Job dict:",ownerNotifDict)
        # return userDict 
        return json.dumps(ownerNotifDict) #return all user data
    
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while getting notification. " + str(e)
            }
        ), 500


# @app.route("/ownerNotification/")
# def get_all():
#     try:
#         jobApp = db.child("jobApp").get()
#         print('this is jobApp', jobApp)
#         jobAppDict = {}    

#         for app in jobApp.each():
#             print(type(app.key()))
#             print("___________") 
#             print("key:",app.key())
#             print("value:",app.val())
#             jobAppDict[app.key()] = app.val()

#         print("Job dict:",jobAppDict)
#         # return userDict 
#         # return json.dumps(jobAppDict) #return all user data

        
#         return jsonify(
#             {
#                 "code": 201,
#                 "data": json.dumps(jobAppDict)
#             }
#             ), 201
    
#     except Exception as e:
#         print("OMG")
#         print(e)

#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred while finding the jobs. " + str(e)
#             }
#         ), 500


# @app.route("/ownerNotified/<string:company_name>", methods = ["POST"])
# def post_noti(company_name):
#     try:
#         data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
#         data = json.loads(data)
#         data["company_name"] = company_name
#         # data.pop("data")
#         print("DATA",data)
#         data["posted_timestamp"] = str(datetime.now())
#         db.child(company_name).push(data)

#         return jsonify(
#             {
#                 "code": 201,
#                 "data": data
#             }
#             ), 201

#     except Exception as e:
#         print("NOO")
#         print(e)

#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred while creating the job. " + str(e)
#             }
#         ), 500
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5010,debug = True)