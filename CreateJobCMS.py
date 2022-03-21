from flask import Flask, request, jsonify

import json
import pyrebase as pb
from invokes import invoke_http
from flask_cors import CORS, cross_origin
import os, sys
import requests

#to remove if we dont use rabbit amqp
#import amqp_setup
#import pika
from flask_cors import CORS

import os, sys
from invokes import invoke_http
import requests


#to remove if we dont use rabbit amqp
#import amqp_setup
import pika
import json



app = Flask(__name__)
CORS(app)


JobsURL = "http://127.0.0.1:5001/jobs"

@app.route("/create_job", methods = ["POST"])
def create_job():
    #if request.is_json:
        try:
            data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
            data = json.loads(data)
            #print(data)
            invoke_http(JobsURL+"/"+data["CID"],method = "POST",json = data)

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
                "code": 201,
                "data": data
            }
            ), 201
      
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " applying for a job...")
    app.run(host="0.0.0.0", port=5009, debug=True)


