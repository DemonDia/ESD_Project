from flask import Flask, request, jsonify
import json
import pyrebase as pb
from invokes import invoke_http
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

# app.config['CORS_HEADERS'] = 'Content-Type'

ApplicationSMS = "http://127.0.0.1:5003/applications"
OwnerStatusSMS = "http://127.0.0.1:5004/status/"

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


@app.route("/get_applications/<string:CID>") # process you auto fill company ID
def owner_get_applications(CID):
    applications = invoke_http(ApplicationSMS+"/company/"+CID,method = "GET")
    return applications



@app.route("/process_application/<string:AID>",methods = ["PUT"]) # process you auto fill company ID
def owner_process_application(AID):
    data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
    data = json.loads(data) #gets
    print(data)
    applications = invoke_http(OwnerStatusSMS+AID,method = "PUT",json = data)
    return jsonify(applications)

def send_to_broker(): #for the broker
    pass

if __name__ == "__main__":
    app.run(port = 5006,debug = True)