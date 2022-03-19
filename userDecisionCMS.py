from flask import Flask, request, jsonify
import json
import pyrebase as pb
from invokes import invoke_http
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

# app.config['CORS_HEADERS'] = 'Content-Type'
ApplicationSMS = "http://127.0.0.1:5003/applications"

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
        return "NOT OK"




if __name__ == "__main__":
    app.run(port = 5005,debug = True)