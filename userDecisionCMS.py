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
JobSMS = "http://127.0.0.1:5001/"
UserStatusSMS = "http://127.0.0.1:5002/applications/"
OwnerNotificationSMS = "http://127.0.0.1:5010/ownerNotified/"
@app.route("/process_application/<string:AID>",methods = ["PUT"])
def processApplication(AID):
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data) #gets
        print(data)
        user_status = invoke_http(UserStatusSMS+AID,json = data,method = "PUT") #returns boolean
        # print("user_status:"+str(user_status))
        print(user_status)

        result = processAMQP(user_status,AID)
        if result['code'] not in range(200, 300):
            # print (result)
            return result

        else:
            if user_status['data'] == True:

                print("AID:"+AID)
                application = invoke_http(ApplicationSMS+"/job/aid/"+AID,method = "GET")
                result = processAMQP(application,AID) #send msg to RabbitMQ

                 #failed to process application
                if result['code'] not in range(200, 300):      
                    return result

                #success, proceed to update vacancy
                else:                           
                    JID  = application["JID"]
                    # return application
                    # JID = application["JID"]
                    # print(application)
                    vacancy = updateVacancy(JID)
                    return vacancy
            else:
                return user_status['data'] #returns false

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

def processAMQP(data,AID):
    if data['code'] not in range(200, 300):
        data['type'] = 'processApp'
        message = json.dumps(data)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="processApp.error", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        # return error
        return {
            "code": 500,
            "result": jsonify(data),
            "message": "process application failure sent for error handling."
        }

    else:
        get_application = invoke_http(ApplicationSMS+"/aid/"+AID,method = "GET")
        application_cid = json.loads(get_application["data"])["CID"]
        # get_application = json.loads(get_application)
        # print("app:",get_application["CID"])
        notiresult = invoke_http(OwnerNotificationSMS+application_cid,method ="POST",json =data)

        # record the activity log anyway
        data['type'] = 'processApp'
        message = json.dumps(data)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="processApp.info", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        return {
            "code": 201,
            "result": jsonify(data),
        }


if __name__ == "__main__":
    app.run(port = 5005,debug = True)