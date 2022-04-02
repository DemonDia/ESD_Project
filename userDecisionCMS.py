from flask import Flask, request, jsonify
import json

import os
from os import environ
import pyrebase as pb
from invokes import invoke_http
import os, sys
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

import direct_amqp_setup
import topic_amqp_setup

import pika

# app.config['CORS_HEADERS'] = 'Content-Type'

# ApplicationSMS = "http://127.0.0.1:5003/applications"
# JobSMS = "http://127.0.0.1:5001/"
# UserStatusSMS = "http://127.0.0.1:5002/applications/"
# OwnerNotificationSMS = "http://127.0.0.1:5010/ownerNotified/"


applicationSMS = environ.get('application_sms') or "http://localhost:5003/applications" 
jobSMS = environ.get('job_sms') or "http://localhost:5001/" 
userStatusSMS = environ.get('userstatus_sms') or "http://localhost:5002/applications/" 
ownerNotificationSMS = environ.get('ownernotification_sms') or "http://localhost:5010/ownerNotified/" 


@app.route("/process_application/<string:AID>",methods = ["PUT"])
# @cross_origin()
def processApplication(AID):
    try:
        print(request)
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data) #gets
        print(data)
        given_application = invoke_http(applicationSMS+"/aid/"+AID,method = "GET")
        JID = json.loads(given_application["data"])["JID"]
        user_status = invoke_http(userStatusSMS+AID,json = data,method = "PUT") #returns boolean
        # print("user_status:"+str(user_status))
        print("user_status",user_status)


        result = processAMQP(user_status,AID,JID)
        print(result)
        if result['code'] not in range(200, 300):
            # print (result)
            return result

        else:
            if user_status['data'] == True:

                print("AID:"+AID)
                application = invoke_http(applicationSMS+"/job/aid/"+AID,method = "GET")
                print("application:",application)
                # result = processAMQP(application,AID,JID) #send msg to RabbitMQ

                 #failed to process application
                if result['code'] not in range(200, 300):      
                    return result

                #success, proceed to update vacancy
                else:                           
                    # JID  = application["JID"]
                    # return application
                    # JID = application["JID"]
                    # print(application)
                    vacancy = updateVacancy(JID)
                    return vacancy
            else:
                return user_status['accepted'] #returns false

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
        print(jobSMS+"update_vacancy/"+JID)
        # print(data)
        
        vacancies = invoke_http(jobSMS+"update_vacancy/"+JID,method = "PUT")
        return str(vacancies)
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating vacancy. " + str(e)
            }
        ), 500

@app.route("/get_applications/<string:user_email>") # process you auto fill company ID
def owner_get_applications(user_email):
    try:
        applications = invoke_http(applicationSMS+"/user/"+user_email,method = "GET")
        return applications
    
    except Exception as e:
        print(e)

        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the job. " + str(e)
            }
        ), 500

def processAMQP(data,AID,JID):
    if data['code'] not in range(200, 300):
        data['type'] = 'processApp'
        message = json.dumps(data)
        topic_amqp_setup.channel.basic_publish(exchange=topic_amqp_setup.exchangename, routing_key="processApp.error", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        # return error
        return {
            "code": 500,
            "result": jsonify(data),
            "message": "process application failure sent for error handling."
        }

    else:
        get_application = invoke_http(applicationSMS+"/aid/"+AID,method = "GET")
        application_name = json.loads(get_application["data"])["company_name"]
        print("output",data)
        data["accepted"] = data["data"]
        # data.pop("data")
        data["AID"] = AID
        data["JID"] = JID
        
        # get_application = json.loads(get_application)
        # print("app:",get_application["CID"])
        print('here', get_application)
        message = json.dumps(get_application['data'])
        direct_amqp_setup.channel.basic_publish(exchange=direct_amqp_setup.exchangename, routing_key="ownerNotification", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        
        # notiresult = invoke_http(OwnerNotificationSMS+application_cid,method ="POST",json =data)

        # record the activity log anyway
        # data.pop('data')
        message = json.dumps(data)
        topic_amqp_setup.channel.basic_publish(exchange=topic_amqp_setup.exchangename, routing_key="processApp.info", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        return {
            "code": 201,
            "result": jsonify(data),
        }

@app.route("/view_job/<JID>", methods = ["GET"])
def view_job(JID):
    if request:
        try:
            #data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 

            # data = json.loads(request.data)
            # print("clean data",data)

            # Send the job info
            job_result = invoke_http(job_sms+"/jobs/"+JID,method = "GET")

            print("result",job_result)

            # record new job
            # record the activity log
            # invoke_http(activity_log_URL,method = "POST",json = job_result)

            # print('my job_result', job_result)

            code = job_result["code"]

            print("code",code)
            print("job result",job_result)

            if code not in range(200, 300):
                #message['type']= "createjob"
                #message = json.dumps(job_result)
                #amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="createjob.error", 
                #body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
                # return error
                return {
                    "code": code,
                    "data": job_result,
                    "message": "Job couldn't be found."
                }
            else:
                
                print("result type",type(job_result))
                return jsonify(
                    {
                        "code": code,
                        "result": job_result["data"]
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
        
    return jsonify(
        {
            "code": 400,
            "data": str(request.get_data())
        }
        ), 400

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " applying for a job...")
    app.run(host="0.0.0.0", port=5005, debug=True)

