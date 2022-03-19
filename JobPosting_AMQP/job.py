#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/job'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Job(db.Model):
    __tablename__ = 'job'

    JID = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(32), nullable=False)
    CID = db.Column(db.Integer, nullable=False)
    datetime_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # modified = db.Column(db.DateTime, nullable=False,
    #                      default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'JID': self.JID,
            'job_title': self.job_title,
            'CID': self.CID,
            'datetime_posted': self.datetime_posted,
        }

        # dto['order_item'] = []
        # for oi in self.order_item:
        #     dto['order_item'].append(oi.json())

        return dto


# class Order_Item(db.Model):
#     __tablename__ = 'order_item'

#     item_id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.ForeignKey(
#         'order.order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

#     book_id = db.Column(db.String(13), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)

#     # order_id = db.Column(db.String(36), db.ForeignKey('order.order_id'), nullable=False)
#     # order = db.relationship('Order', backref='order_item')
#     order = db.relationship(
#         'Order', primaryjoin='Order_Item.order_id == Order.order_id', backref='order_item')

#     def json(self):
#         return {'item_id': self.item_id, 'book_id': self.book_id, 'quantity': self.quantity, 'order_id': self.order_id}


@app.route("/job")
def get_all():
    joblist = Job.query.all()
    if len(joblist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "jobs": [job.json() for job in joblist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404


@app.route("/job/<string:JID>")
def find_by_job_id(JID):
    job = Job.query.filter_by(JID=JID).first()
    if job:
        return jsonify(
            {
                "code": 200,
                "data": job.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "JID": JID
            },
            "message": "Order not found."
        }
    ), 404


@app.route("/job", methods=['POST'])
def create_job():
    JID = request.json.get('JID', None)
    job_title = request.json.get('job_title', None)
    CID = request.json.get('CID', None)
    datetime_posted = request.json.get('datetime_posted', None)
    job = Job(JID=JID, job_title=job_title, CID=CID, datetime_posted=datetime_posted)

    # cart_item = request.json.get('cart_item')
    # for item in cart_item:
    #     order.order_item.append(Order_Item(
    #         book_id=item['book_id'], quantity=item['quantity']))

    try:
        db.session.add(job)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500
    
    print(json.dumps(job.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": job.json()
        }
    ), 201


@app.route("/job/<string:JID>", methods=['PUT'])
def update_job(JID):
    try:
        job = Job.query.filter_by(JID=JID).first()
        if not job:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "JID": JID
                    },
                    "message": "Job not found."
                }
            ), 404

        # update status
        # data = request.get_json()
        # if data['status']:
        #     job.status = data['status']
        #     db.session.commit()
        #     return jsonify(
        #         {
        #             "code": 200,
        #             "data": order.json()
        #         }
        #     ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "JID": JID
                },
                "message": "An error occurred while updating the job. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage job ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
