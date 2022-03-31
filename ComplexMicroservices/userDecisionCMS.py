from flask import Flask, request, jsonify
import json
import pyrebase as pb
from invokes import invoke_http
from flask_cors import CORS,cross_origin
import os
from os import environ
app = Flask(__name__)
CORS(app)

# app.config['CORS_HEADERS'] = 'Content-Type'
# ApplicationSMS = "http://127.0.0.1:5003/applications"
# JobSMS = "http://127.0.0.1:5001/"
# UserStatusSMS = "http://127.0.0.1:5002/applications/"
# OwnerNotificationSMS = "http://127.0.0.1:5010/ownerNotified/"


ApplicationSMS = environ.get("ApplicationSMS") or "http://localhost:5003/applications"
JobSMS = environ.get("JobSMS") or "http://localhost:5001/"
UserStatusSMS = environ.get("UserStatusSMS") or "http://localhost:5002/applications/"
OwnerNotificationSMS = environ.get("OwnerNotificationSMS") or "http://localhost:5010/ownerNotified/"

@app.route("/process_application/<string:AID>",methods = ["PUT"])
def processApplication(AID):
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data) #gets
        print(data)
        user_status = invoke_http(UserStatusSMS+AID,json = data,method = "PUT") #returns boolean
        # print("user_status:"+str(user_status))
        if user_status == True:
            print("AID:"+AID)
            application = invoke_http(ApplicationSMS+"/job/aid/"+AID,method = "GET")
            JID  = application["JID"]
            # return application
            # JID = application["JID"]
            # print(application)
            vacancy = updateVacancy(JID)
            return vacancy

        else:
            return str(user_status) #returns false
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while processing the application " + str(e)
            }
        ), 500

def updateVacancy(JID):
    print("JID:"+JID)
    try:
        print(JobSMS+"update_vacancy/"+JID)
        # print(data)
        
        vacancies = invoke_http(JobSMS+"update_vacancy/"+JID,method = "PUT")
        return str(vacancies)
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating vacancy. " + str(e)
            }
        ), 500

@app.route("/get_applications/<string:UID>") # process you auto fill company ID
def owner_get_applications(UID):
    try:
        applications = invoke_http(ApplicationSMS+"/user/"+UID,method = "GET")
        return applications
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the job. " + str(e)
            }
        ), 500


if __name__ == "__main__":
    app.run(port = 5005,debug = True)