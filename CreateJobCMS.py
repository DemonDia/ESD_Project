from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from invokes import invoke_http
import requests


#to remove if we dont use rabbit amqp
import amqp_setup
import pika
import json



app = Flask(__name__)
CORS(app)


create_job_URL = "http://127.0.0.1:5001/jobs"
# check if job is there

@app.route("/create_job/<string:CID>",methods = ["POST"])
def create_job(CID):
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data)
        print(data)
        invoke_http(create_job_URL,method = "POST",json = data)
        return "OK"
    except Exception as e:
        print(e)
        return "NOT OK"



# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " applying for a job...")
    app.run(host="0.0.0.0", port=5009, debug=True)


