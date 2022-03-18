from crypt import methods
from flask import Flask, request, jsonify
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


@app.route("/jobs") # get all jobs
def get_all():
    try:
        jobs = db.child("jobs").get()
        jobsDict = {}        
                
    
        for job in jobs.each():
            print(type(job.key()))
            print("___________") 
            print("key:",job.key())
            print("value:",job.val())
            jobsDict[job.key()] = job.val()
        # return userDict
        return jobsDict #return all user data
    except Exception as e:
        return e







if __name__ == "__main__":
    app.run(port = 5000,debug = True)