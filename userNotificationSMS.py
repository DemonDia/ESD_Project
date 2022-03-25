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

# db.create_all()

# {
#    "JID": "-MyVtBZxF7DzNc969y7_", 
#    "UID": "666666"
# }

@app.route("/userNotification")
def get_all():
    try:
        jobApp = db.child("jobApp").get()
        print('this is jobApp', jobApp)
        jobAppDict = {}    

        for app in jobApp.each():
            print(type(app.key()))
            print("___________") 
            print("key:",app.key())
            print("value:",app.val())
            jobAppDict[app.key()] = app.val()

        print("Job dict:",jobAppDict)
        # return userDict 
        return json.dumps(jobAppDict) #return all user data
    
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while getting notification. " + str(e)
            }
        ), 500


@app.route("/userNotification/<string:CID>", methods = ["POST"])
def post_noti(CID):
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data)
        print(type(data))
        data["posted_timestamp"] = str(datetime.now())
        db.child(CID).push(data)

        return jsonify(
            {
                "code": 201,
                "data": data
            }
            ), 201

    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while posting the user's notification. " + str(e)
            }
        ), 500
    
    

if __name__ == "__main__":
    app.run(port = 5010,debug = True)