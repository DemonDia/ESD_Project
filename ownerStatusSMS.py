from flask import Flask, request, jsonify
import json
import pyrebase as pb

from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

# app.config['CORS_HEADERS'] = 'Content-Type'


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
@app.route("/status/<string:AID>",methods = ["PUT"]) # create_app
def owner_process_application(AID):
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data) #gets
        db.child("applications/"+AID).update({"app_status":data["app_status"]})
        return data["app_status"]
        # return decision
    except Exception as e:
        print(e)
        return "NOT OK"




if __name__ == "__main__":
    app.run(port = 5004,debug = True)