from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

#book_URL = "http://localhost:5000/book"
job_URL = "http://localhost:5001/job"
# shipping_record_URL = "http://localhost:5002/shipping_record"
#activity_log_URL = "http://localhost:5003/activity_log"
#error_URL = "http://localhost:5004/error"


@app.route("/create_job", methods=['POST'])
def create_job():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            job = request.get_json()
            print("\nReceived a job in JSON:", job)

            # do the actual work
            # 1. Send job info {job details}
            result = processCreateJob(job)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
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


def processCreateJob(job):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    print('\n-----Invoking job microservice-----')
    job_result = invoke_http(job_URL, method='POST', json=job)
    print('job_result:', job_result)
  

    # Check the order result; if a failure, send it to the error microservice.
    code = job_result["code"]
    message = json.dumps(job_result)

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (job error) message with routing_key=job.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="job.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\Job status ({:d}) published to the RabbitMQ Exchange:".format(
            code), job_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"job_result": job_result},
            "message": "Job creation failure sent for error handling."
        }

    # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # In http version, we first invoked "Activity Log" and then checked for error.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

    else:
        # 4. Record new order
        # record the activity log anyway
        #print('\n\n-----Invoking activity_log microservice-----')
        print('\n\n-----Publishing the (job info) message with routing_key=job.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="job.info", 
            body=message)
    
    print("\nJob published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails
    
    # # 5. Send new order to shipping
    # # Invoke the shipping record microservice
    # print('\n\n-----Invoking shipping_record microservice-----')    
    
    # shipping_result = invoke_http(
    #     shipping_record_URL, method="POST", json=order_result['data'])
    # print("shipping_result:", shipping_result, '\n')

    # # Check the shipping result;
    # # if a failure, send it to the error microservice.
    # code = shipping_result["code"]
    # if code not in range(200, 300):
    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as shipping fails-----')
    #     print('\n\n-----Publishing the (shipping error) message with routing_key=shipping.error-----')

    #     # invoke_http(error_URL, method="POST", json=shipping_result)
    #     message = json.dumps(shipping_result)
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="shipping.error", 
    #         body=message, properties=pika.BasicProperties(delivery_mode = 2))

    #     print("\nShipping status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), shipping_result)

    #     # 7. Return error
    #     return {
    #         "code": 400,
    #         "data": {
    #             "order_result": order_result,
    #             "shipping_result": shipping_result
    #         },
    #         "message": "Simulated shipping record error sent for error handling."
    #     }

    # 7. Return created order, shipping record
    return {
        "code": 201,
        "data": {
            "job_result": job_result,
        }
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for creating an job...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
