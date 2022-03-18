from crypt import methods
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import pyrebase as pb
app = Flask(__name__)
CORS(app)
# sqlalchemy

# dialect+driver://username:password@host:port/database


firebaseConfig = {
    "apiKey": "AIzaSyATNL8Kmwu9OcnT_kIf-I_6Jy_oyPtH6qk",
    "authDomain": "usermicroservice-6f100.firebaseapp.com",
    "databaseURL": "https://usermicroservice-6f100-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "usermicroservice-6f100",
    "storageBucket": "usermicroservice-6f100.appspot.com",
    "messagingSenderId":  "660450931889",
    "appId": "1:660450931889:web:0ea383811be60b73561e90"
}

firebase = pb.initialize_app(firebaseConfig)
db = firebase.database() #user realtime db

# db.create_all()


@app.route("/apps/<string:jobID>",methods = ["POST"]) # create_app
def create_application(jobID):
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data)
        print(data)

        db.child("applications").push(data)
        return "OK"
    except:
        return "NOT OK"


def get_all():
    try:
        applications = db.child("applications").get()
        applicationsDict = {}        
                
    
        for application in applications.each():
            print(type(application.key()))
            print("___________") 
            print("key:",application.key())
            print("value:",application.val())
            applicationsDict[job.key()] = application.val()
        # return userDict
        return applicationsDict #return all user data
    except Exception as e:
        return e