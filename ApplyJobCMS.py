from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from invokes import invoke_http
import requests


#to remove if we dont use rabbit amqp
# import amqp_setup
import pika
import json



app = Flask(__name__)
CORS(app)


JobsURL = "http://127.0.0.1:5001/jobs"
ApplicationURL = "http://127.0.0.1:5003/applications/"
# check if job is there



@app.route("/apply_job", methods=['POST'])
def apply_job():
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data)
        print(data)
        print(JobsURL+"/"+data["JID"])
        result = invoke_http(JobsURL+"/"+data["JID"],method ="GET")
        result = jsonify(result)
        if(result == "404"):
            # message = result["code"]
            # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="job.error", 
            # body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
            return "NOT OK"
        else:
            result = invoke_http(ApplicationURL+data["JID"],method ="POST",json =data)
            # print(result)
        return "OK"
    except Exception as e:
        print(e)
        return "NOT OK"




# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " applying for a job...")
    app.run(host="0.0.0.0", port=5008, debug=True)


