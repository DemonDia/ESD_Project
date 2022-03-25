from flask import Flask, request, jsonify
import json
import pyrebase as pb
from invokes import invoke_http
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

import amqp_setup
import pika

# app.config['CORS_HEADERS'] = 'Content-Type'

ApplicationSMS = "http://127.0.0.1:5003/applications"
OwnerStatusSMS = "http://127.0.0.1:5004/status/"



@app.route("/get_applications/<string:CID>") # process you auto fill company ID
def owner_get_applications(CID):
    try:
        applications = invoke_http(ApplicationSMS+"/company/"+CID,method = "GET")
        # return applications

        return jsonify(
            {
                "code": 201,
                "data": jsonify(applications)
            }
            ), 201

    except Exception as e:
        # return "NOT OK"

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while obtaining the application. " + str(e)
            }
        ), 500



@app.route("/process_application/<string:AID>",methods = ["PUT"]) # process you auto fill company ID
def owner_process_application(AID):
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data) #gets
        print(data)
        applications = invoke_http(OwnerStatusSMS+AID,method = "PUT",json = data)
        # return jsonify(applications)

        if applications['code'] not in range(200, 300):
            message = json.dumps(applications)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="updateApp.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            # return error
            return {
                "code": 500,
                "result": jsonify(applications),
                "message": "Update application failure sent for error handling."
            }

        else:
            # record the activity log anyway
            message = json.dumps(applications)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="updateApp.info", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            return jsonify(
                {
                    "code": 201,
                    "result": jsonify(applications)
                }
                ), 201

    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the job. " + str(e)
            }
        ), 500

def send_to_broker(): #for the broker
    pass

if __name__ == "__main__":
    app.run(port = 5006,debug = True)