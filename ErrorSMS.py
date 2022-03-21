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
    "apiKey": "AIzaSyC6vFvSWpcY6sS8g1nXvWC3Rgo3X_ZwrqY",
    "authDomain": "errormicroservice.firebaseapp.com",
    "projectId": "errormicroservice",
    "storageBucket": "errormicroservice.appspot.com",
    "messagingSenderId": "356092494930",
    "appId": "1:356092494930:web:22814fccd220402ae00b8b"
}

firebase = pb.initialize_app(firebaseConfig)
db = firebase.database() #user realtime db

# db.create_all()
@app.route("/errors", methods=['POST']) # create activities
def create_error():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            errors = request.get_json()
            print("\nReceived a error in JSON:", errors)
            errors = json.loads(errors)
            db.child("errors").push(errors)
            
            return jsonify({
                "code": 200,
                "data": {"errors": errors},
                "message": "errors creation successful"
            })

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_error.py internal error: " + ex_str
            }), 500
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


@app.route("/errors")
def get_all():
    errors = db.child("errors").get()

    errorsDict = {}

    for error in errors.each():
        errorsDict[error.key()] = error.val()

    if errorsDict != {}:
        try:
            errors = db.child("errors").get()
            print(errors)
            errorsDict = {}

            for error in errors.each():
                errorsDict[error.key()] = error.val()

            print(errorsDict)

            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "errors": [errorsDict]
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
                "message": "ErrorSMS.py internal error: " + ex_str
            }), 500

    return jsonify(
        {
            "code": 404,
            "message": "There are no errors."
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
