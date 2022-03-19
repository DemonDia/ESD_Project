from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

#to remove if we dont use rabbit amqp
#import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

create_job_URL = "http://localhost:5001/jobs"

@app.route("/job", methods=['POST'])
def create_job():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            job = request.get_json()
            print("\nReceived 1 Job information in JSON:", job)

            # do the actual work
            # 1. Send Job info {job_info}
            result = processJob(job)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type,exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "create_job.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processJob(job):
    # 2. Send the job info {job_info}
    # Invoke the Job microservice
    print('\n-----Invoking Job microservice-----')
    job_result = invoke_http(create_job_URL, method='POST', json=job)
    print('job_result: ', job_result)

    # Check the job result; if a failure, send it to the error microservice.
    code = job_result["code"]
    message = json.dumps(job_result)

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (job error) message with routing_key=job.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        #amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="job.error", body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nJob status ({:d}) published to the RabbitMQ Exchange:".format(
            code), job_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"job_result": job_result},
            "message": "Job creation failure sent for error handling."
        }

    #publishing to Activity Log only when there is no error
    #binding key # is used as any routing_key would be matched

    else:
        # 4. Record new Job
        # record the activity log anyway
        print('\n\n-----Invoking activity_log microservice-----')
        print('\n\n-----Publishing the (job info) message with routing_key=job.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=job_result)            
        #amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="job.info", body=message)

    print("\nJob published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)


