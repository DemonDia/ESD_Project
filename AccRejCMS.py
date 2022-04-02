from flask import Flask, request, jsonify
import json
import pyrebase as pb
import os, sys
from os import environ
from invokes import invoke_http
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

import direct_amqp_setup
import topic_amqp_setup
import pika

# app.config['CORS_HEADERS'] = 'Content-Type'

# applicationSMS = "http://127.0.0.1:5003/applications"
# ownerStatusSMS = "http://127.0.0.1:5004/status/"
# userNotificationSMS = "http://127.0.0.1:5011/userNotification/"

applicationSMS = environ.get('application_sms') or "http://localhost:5003/applications" 
ownerStatusSMS = environ.get('ownerstatus_sms') or "http://localhost:5004/status/" 
userNotificationSMS = environ.get('usernotification_sms') or "http://localhost:5011/userNotification/" 

@app.route("/get_applications/<string:CompanyName>") # process you auto fill company ID
def owner_get_applications(CompanyName):
    try:
        applications = invoke_http(applicationSMS+"/company/"+CompanyName,method = "GET")
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
        applications = invoke_http(applicationSMS+"/aid/"+AID,method = "GET")
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
        print("this is data",data)
        applications = invoke_http(ownerStatusSMS+AID,method = "PUT",json = data)
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
    print(applicationSMS+"/aid/"+AID)
    get_application = invoke_http(applicationSMS+"/aid/"+AID,method = "GET")
    get_application = json.loads(get_application["data"])
    print(get_application)

    data["company_name"] = get_application["company_name"]
    data["JID"] = get_application["JID"]

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
