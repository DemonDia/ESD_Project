from flask import Flask, request, jsonify
import json
import pyrebase as pb
<<<<<<< HEAD:ComplexMicroservices/AccRejCMS.py
<<<<<<< Updated upstream:AccRejCMS.py
=======
import os
from os import environ
>>>>>>> Stashed changes:ComplexMicroservices/AccRejCMS.py
=======
import os, sys
>>>>>>> main:AccRejCMS.py
from invokes import invoke_http
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

import direct_amqp_setup
import topic_amqp_setup
import pika

# app.config['CORS_HEADERS'] = 'Content-Type'

<<<<<<< Updated upstream:AccRejCMS.py
ApplicationSMS = "http://127.0.0.1:5003/applications"
OwnerStatusSMS = "http://127.0.0.1:5004/status/"
<<<<<<< HEAD:ComplexMicroservices/AccRejCMS.py
=======
# ApplicationSMS = "http://127.0.0.1:5003/applications"
# OwnerStatusSMS = "http://127.0.0.1:5004/status/"
# UserNotiURL ="http://127.0.0.1:5011/status/"
>>>>>>> Stashed changes:ComplexMicroservices/AccRejCMS.py

ApplicationSMS = environ.get("ApplicationSMS") or "http://localhost:5003/applications"
OwnerStatusSMS = environ.get("OwnerStatusSMS") or "http://localhost:5004/status/"
UserNotiURL = environ.get("UserNotiURL") or "http://localhost:5011/applications"
=======
UserNotiURL = "http://127.0.0.1:5011/userNotification/"

>>>>>>> main:AccRejCMS.py


@app.route("/get_applications/<string:CID>") # process you auto fill company ID
def owner_get_applications(CID):
    try:
        applications = invoke_http(ApplicationSMS+"/company/"+CID,method = "GET")
        return applications

    except Exception as e:
        # return "NOT OK"

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while obtaining the application. " + str(e)
            }
        ), 500

@app.route("/get_app/<string:AID>") # process you auto fill company ID
def owner_get_app(AID):
    try:
        applications = invoke_http(ApplicationSMS+"/aid/"+AID,method = "GET")
        return applications

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
        # get 
        
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data) #gets
        print(data)
        applications = invoke_http(OwnerStatusSMS+AID,method = "PUT",json = data)
        print(applications)
        # print(applications['code'])
        # return jsonify(applications)


        if applications['code'] not in range(200, 300):
            message = json.dumps(applications)
            topic_amqp_setup.channel.basic_publish(exchange=topic_amqp_setup.exchangename, routing_key="updateApp.error", 
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
            notifySeeker(data)
            notifySeeker(AID,data)
            topic_amqp_setup.channel.basic_publish(exchange=topic_amqp_setup.exchangename, routing_key="updateApp.info", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            return jsonify(applications)

    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while processing the application. " + str(e)
            }
        ), 500

# def send_to_broker(): #for the broker
#     pass
def notifySeeker(AID,data):
    print(ApplicationSMS+"/aid/"+AID)
    get_application = invoke_http(ApplicationSMS+"/aid/"+AID,method = "GET")
    get_application = json.loads(get_application["data"])
    print(get_application)

    data["CID"] = get_application["CID"]
    data["JID"] = get_application["JID"]
    data["UID"] = get_application["UID"]

    # New: AMQP broker send message to user notification
    message = json.dumps(get_application)
    direct_amqp_setup.channel.basic_publish(exchange=direct_amqp_setup.exchangename, routing_key="userNotification", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    # get_application = json.loads(get_application)
    # print("app:",get_application["CID"])
    # notiresult = invoke_http(UserNotiURL+get_application["CID"],method ="POST",json =data)
    # notiresult['type'] = 'ownerNoti'
    # message = json.dumps(notiresult)
    # if notiresult["code"] not in range(200, 300):
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="ownerNoti.error", 
    #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    #     # return error
    #     return jsonify(
    #         {
    #             "code": 500,
    #             "data": message
    #         }), 500
    # else:
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="ownerNoti.info", 
    #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    #     # return error
    #     return jsonify(
    #         {
    #             "code": 200,
    #             "data": message
    #         }), 200

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " applying for a job...")
    app.run(host="0.0.0.0", port=5006, debug=True)
