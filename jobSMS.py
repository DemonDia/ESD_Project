#from crypt import methods
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pyrebase as pb
import json

app = Flask(__name__)
CORS(app)
# sqlalchemy

# dialect+driver://username:password@host:port/database

firebaseConfig = {
  "apiKey": "AIzaSyCCD_YMl1GVhCacEWtj424cMrmqHWqyzw0",
  "authDomain": "jobmicroservice-13a0c.firebaseapp.com",
  "databaseURL": "https://jobmicroservice-13a0c-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "jobmicroservice-13a0c",
  "storageBucket": "jobmicroservice-13a0c.appspot.com",
  "messagingSenderId": "209394015065",
  "appId": "1:209394015065:web:b6612fd69caeaea6124a48"
}

firebase = pb.initialize_app(firebaseConfig)
db = firebase.database() #user realtime db

# db.create_all()

#get all jobs
@app.route("/jobs") 
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
        print("Job dict:",jobsDict)
        # return userDict
        return json.dumps(jobsDict) #return all user data
    
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while finding the jobs. " + str(e)
            }
        ), 500

#create 1 job
@app.route("/jobs/<string:CID>",methods = ["POST"])
def post_job(CID):


        return "NOT OK"

@app.route("/jobs/create_job",methods = ["POST"])
def post_job():

    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data)
        print(type(data))
        data["posted_timestamp"] = str(datetime.now())
        db.child("jobs").child(CID).push(data)

    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the job. " + str(e)
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            "data": data
        }
        ), 201

#get job by .. (need to fix)
@app.route("/jobs/<string:JobID>")
def get_job_by_id(JobID):
    try:
        job = db.child("jobs/"+JobID).get()
        jobDict = {}

        jobDict[job.key()] = job.val()
        print(jobDict[JobID])
        # print(user.key())
        print(bool(jobDict[JobID])) #return true and false
        
    # bool(userDict["users"])

        if(bool(jobDict[JobID])): #yes theres an existing user
            return json.dumps(jobDict)
        else:
            return "404"  #empty user valu

    except:

        return "NOT OK"

if __name__ == "__main__":
    app.run(port = 5001,debug = True)