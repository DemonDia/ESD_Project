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

@app.route("/applications/<string:AID>",methods = ["PUT"]) # create_app
def processApplication(AID):
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data) #gets
        print(data)
        db.child("applications/"+AID).update({"user_dec":data["user_dec"]})
        
        return jsonify({
            "code": 201,
            "data": str(data["user_dec"])
        }), 201

        # return decision
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while processing the application " + str(e)
            }
        ), 500




if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5002,debug = True)