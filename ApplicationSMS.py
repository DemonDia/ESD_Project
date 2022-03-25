# from crypt import methods
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import pyrebase as pb
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


@app.route("/applications/<string:JID>",methods = ["POST"]) # create_app
def create_application(JID):
    try:

        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data)
        data["JID"] = JID
        # print(data)

        db.child("applications").push(data)
        # return "OK"
        return jsonify(
                {
                    "code": 201,
                    "data": json.dumps(data)
                }
                ), 201
    except Exception as e:
        print(e)
        # return "NOT OK"
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while applying for job. " + str(e)
            }
        ), 500

@app.route("/applications")
def get_all():
    try:
        applications = db.child("applications").get()
        applicationsDict = {}        
                
    
        for application in applications.each():
            print(type(application.key()))
            print("___________") 
            print("key:",application.key())
            print("value:",application.val())
            applicationsDict[application.key()] = application.val()
        # return userDict
        # return json.dumps(applicationsDict) #return all user data

        return jsonify(
            {
                "code": 201,
                "data": json.dumps(applicationsDict)
            }
            ), 201

    except Exception as e:
        print(e)
        # return "NOT OK"

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while applying for job. " + str(e)
            }
        ), 500

@app.route("/applications/job/<string:JID>") # get all applications to certain jobs
def get_application_by_JID(JID):
    try:
        applications = db.child("applications").order_by_child("JID").equal_to(JID).get()
        applicationsDict = {}        
                
    
        for application in applications.each():
            print(type(application.key()))
            print("___________") 
            print("key:",application.key())
            print("value:",application.val())
            applicationsDict[application.key()] = application.val()
        # print("Job dict:",applicationsDict)
        # return userDict
        # return json.dumps(applicationsDict) #return all user data

        return jsonify(
            {
                "code": 201,
                "data": json.dumps(applicationsDict)
            }
            ), 201

    except Exception as e:
        print(e)
        # return "NOT OK"
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while obtaining applications. " + str(e)
            }
        ), 500


@app.route("/applications/job/aid/<string:AID>") # get applications based on AID
def get_application_by_AID(AID):
    try:
        applications = db.child("applications/"+AID).get()
        applicationsDict = {}        
                
    
        for application in applications.each():
            print(type(application.key()))
            print("___________") 
            print("key:",application.key())
            print("value:",application.val())
            applicationsDict[application.key()] = application.val()
        # print("Job dict:",applicationsDict)
        # return userDict
        # return json.dumps(applicationsDict) #return all user data

        return jsonify(
            {
                "code": 201,
                "data": json.dumps(applicationsDict)
            }
            ), 201

    except Exception as e:
        print(e)
        # return "NOT OK"
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while obtaining application. " + str(e)
            }
        ), 500


@app.route("/applications/company/<string:CID>") # get all applications to certain company
def get_all_applications_of_a_company(CID):
    try:
        applications = db.child("applications").order_by_child("CID").equal_to(CID).get()
        applicationsDict = {}        
                
    
        for application in applications.each():
            print(type(application.key()))
            print("___________") 
            print("key:",application.key())
            print("value:",application.val())
            applicationsDict[application.key()] = application.val()
        # print("Job dict:",applicationsDict)
        # return userDict
        # return json.dumps(applicationsDict) #return all user data

        return jsonify(
            {
                "code": 201,
                "data": json.dumps(applicationsDict)
            }
            ), 201
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while obtaining applications. " + str(e)
            }
        ), 500

@app.route("/applications/user/<string:UID>") # get jobs user applied to
def get_all_applications_of_a_user(UID):
    try:
        applications = db.child("applications").order_by_child("UID").equal_to(UID).get()
        applicationsDict = {}        
                
    
        for application in applications.each():
            print(type(application.key()))
            print("___________") 
            print("key:",application.key())
            print("value:",application.val())
            applicationsDict[application.key()] = application.val()
        # print("Job dict:",applicationsDict)
        # return userDict
        # return json.dumps(applicationsDict) #return all user data
        return jsonify(
            {
                "code": 201,
                "data": json.dumps(applicationsDict)
            }
            ), 201
            
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while processing the application " + str(e)
            }
        ), 500


if __name__ == "__main__":
    app.run(port = 5003,debug = True)