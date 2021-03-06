from flask import Flask, request, jsonify

import json
import pyrebase as pb
from invokes import invoke_http
from flask_cors import CORS, cross_origin
import os, sys
from os import environ
import requests

#to remove if we dont use rabbit amqp
import direct_amqp_setup
import topic_amqp_setup
import pika
from flask_cors import CORS

import os, sys
from invokes import invoke_http
import requests


#to remove if we dont use rabbit amqp
# import amqp_setup
# import pika
#import json



app = Flask(__name__)
CORS(app)


# jobSMS = "http://127.0.0.1:5001/jobs"
# activity_log_URL = "http://127.0.0.1:5010/activities"

jobSMS = environ.get('job_sms') or "http://localhost:5001/jobs" 
# applicatioNSMS = environ.get('applicatioNSMS') or "http://localhost:5003/applications/" 
# ownerNotifiationSMS = environ.get('ownerNotifiationSMS') or "http://localhost:5010/ownerNotification/" 



@app.route("/create_job", methods = ["POST"])
def create_job():
    if request:
        try:
            data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
            print(data)
            data = json.loads(request.data)
            # Send the job info
            job_result = invoke_http(jobSMS+"/create",method = "POST",json = data)

            # record new job
            # record the activity log
            # invoke_http(activity_log_URL,method = "POST",json = job_result)

            # print('my job_result', job_result)

            code = job_result["code"]
            if code not in range(200, 300):
                # message['type']= "createjob"
                dict1 = {"message": "Creation of job failure"}
                job_result['data'].update(dict1)
                message = json.dumps(job_result["data"])
                topic_amqp_setup.channel.basic_publish(exchange=topic_amqp_setup.exchangename, routing_key="createjob.error", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            print("code",code)
            print("job result",job_result)

            if code not in range(200, 300):
                #message['type']= "createjob"
                #message = json.dumps(job_result)
                #amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="createjob.error", 
                #body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
                # return error
                return job_result

            else:
                # Record new job
                # record the activity log anyway
                # message['type']= "createjob"
                dict2 = {"message": "job created successfully"}
                job_result['data'].update(dict2)
                print('this one after adding ', job_result)
                message = json.dumps(job_result["data"])
                topic_amqp_setup.channel.basic_publish(exchange=topic_amqp_setup.exchangename, routing_key="createjob.info", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

                return job_result

        except Exception as e:
            print(e)

            message = json.dumps({
                "code": 500,
                "message": "An error occurred while creating the job. " + str(e)
                })
            topic_amqp_setup.channel.basic_publish(exchange=topic_amqp_setup.exchangename, routing_key="createjob.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            return json.loads(message)
        
    return jsonify(
        {
            "code": 400,
            "data": str(request.get_data())
        }
        ), 400


      
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " applying for a job...")
    app.run(host="0.0.0.0", port=5009, debug=True)


