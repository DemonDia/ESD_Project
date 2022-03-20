#from crypt import methods
import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import pyrebase as pb
import json
app = Flask(__name__)
CORS(app)
# sqlalchemy

# dialect+driver://username:password@host:port/database

firebaseConfig = {
  "apiKey": "AIzaSyAJyo8v_ol6NZwDkYzj9R7-tIn2q8IyiP4",
  "authDomain": "activitymicroservice.firebaseapp.com",
  "databaseURL": "https://activitymicroservice-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "activitymicroservice",
  "storageBucket": "activitymicroservice.appspot.com",
  "messagingSenderId": "230760775714",
  "appId": "1:230760775714:web:9ef96d00b609383d1f8a7b"
}

firebase = pb.initialize_app(firebaseConfig)
db = firebase.database() #user realtime db

# db.create_all()
@app.route("/activities", methods=['POST']) # create activities
def create_activities():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            activities = request.get_json()
            print("\nReceived a activities in JSON:", activities)
            activities = json.loads(activities)
            db.child("activities").push(activities)
            
            return jsonify({
                "code": 200,
                "data": {"activities": activities},
                "message": "Activities creation successful"
            })

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_activities.py internal error: " + ex_str
            }), 500
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


@app.route("/activities")
def get_all():
    activities = db.child("activities").get()

    activitiesDict = {}

    for activity in activities.each():
        activitiesDict[activity.key()] = activity.val()

    if activitiesDict != {}:
        try:
            activities = db.child("activities").get()
            print(activities)
            activitiesDict = {}

            for activity in activities.each():
                activitiesDict[activity.key()] = activity.val()

            print(activitiesDict)

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "activities": [activitiesDict]
                    }
                }
            )

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "ActivitySMS.py internal error: " + ex_str
            }), 500

    return jsonify(
        {
            "code": 404,
            "message": "There are no activities."
        }
    ), 404


# @app.route("/job/<string:JID>")
# def find_by_job_id(JID):
#     job = Job.query.filter_by(JID=JID).first()
#     if job:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": job.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "JID": JID
#             },
#             "message": "Order not found."
#         }
#     ), 404


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage job ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
