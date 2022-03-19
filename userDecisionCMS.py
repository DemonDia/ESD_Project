from flask import Flask, request, jsonify
import json
import pyrebase as pb
from invokes import invoke_http
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

# app.config['CORS_HEADERS'] = 'Content-Type'
ApplicationSMS = "http://127.0.0.1:5003/applications"

firebaseConfig = {
  "apiKey": "AIzaSyCCD_YMl1GVhCacEWtj424cMrmqHWqyzw0",
  "authDomain": "jobmicroservice-13a0c.firebaseapp.com",
  "databaseURL": "https://jobmicroservice-13a0c-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "jobmicroservice-13a0c",
  "storageBucket": "jobmicroservice-13a0c.appspot.com",
  "messagingSenderId": "209394015065",
  "appId": "1:209394015065:web:b6612fd69caeaea6124a48"
}

@app.route("/get_applications")
def getUsers(UID):
    try:
        pass
    except:
        pass
@app.route("/get_applications/<string:UID>") # process you auto fill company ID
def owner_get_applications(UID):
    try:
        applications = invoke_http(ApplicationSMS+"/user/"+UID,method = "GET")
        return applications
    except Exception as e:
        return None




if __name__ == "__main__":
    app.run(port = 5005,debug = True)