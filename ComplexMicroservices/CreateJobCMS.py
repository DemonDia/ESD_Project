from flask import Flask, request, jsonify

import json
import pyrebase as pb
from invokes import invoke_http
from flask_cors import CORS, cross_origin
import os
from os import environ

#to remove if we dont use rabbit amqp
import amqp_setup
import pika
from flask_cors import CORS

import os, sys
from invokes import invoke_http
import requests


#to remove if we dont use rabbit amqp
#import amqp_setup
#import pika
#import json



app = Flask(__name__)
CORS(app)


# JobsURL = "http://127.0.0.1:5001/jobs"
# activity_log_URL = "http://127.0.0.1:5010/activities"
JobsURL = environ.get("JobsURL") or "http://localhost:5001/jobs"
JobsURL = environ.get("activity_log_URL") or "http://localhost:5010/activities"
@app.route("/create_job", methods = ["POST"])
def create_job():
    if request.is_json:
        try:
            data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
            data = json.loads(data)
            print(data)

            # Send the job info
            job_result = invoke_http(JobsURL+"/create",method = "POST",json = data)

            # print(job_result)

            # record new job
            # record the activity log
            # invoke_http(activity_log_URL,method = "POST",json = job_result)

            # print('my job_result', job_result)

            code = job_result["code"]
            if code not in range(200, 300):
                message = json.dumps(job_result)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="createjob.error", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

                # return error
                return {
                    "code": 500,
                    "data": {"job_result": job_result},
                    "message": "Job creation failure sent for error handling."
                }
            else:
                # Record new job
                # record the activity log anyway
                message = json.dumps(job_result)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="createjob.info", 
                body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

                return jsonify(
                    {
                        "code": 201,
                        "result": job_result
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
      
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " applying for a job...")
    app.run(host="0.0.0.0", port=5009, debug=True)


