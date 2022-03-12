from crypt import methods
from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# sqlalchemy

# dialect+driver://username:password@host:port/database
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://bfec0a26f11d48:80c4f19c@us-cdbr-east-05.cleardb.net/heroku_a81f2a9c8a876ab?"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# db.create_all()
class Job(db.Model):
    __tablename__ = 'job_posting'
 
    jobID = db.Column(db.String(13), primary_key=True)
    jobTitle = db.Column(db.String(64), nullable=False)
    company = db.Column(db.String(64), nullable=False)
    employmentType = db.Column(db.String(24), nullable=False)
    industry = db.Column(db.String(64), nullable=False)
    salary = db.Column(db.Numeric(6,2), nullable=False)
 
    def __init__(self,jobID, jobTitle, company, employmentType, industry,salary):
        self.jobID = jobID
        self.jobTitle = jobTitle
        self.company = company
        self.employmentType = employmentType
        self.industry = industry
        self.salary = salary

 
    def json(self):
        return {
            "jobID": self.jobID, "jobTitle": self.jobTitle, 
            "company": self.company, "employmentType": self.employmentType, 
            "industry": self.industry, "salary": self.salary
            }

@app.route("/jobs") # get all jobs
def get_all():
    jobList = Job.query.all()
    if len(jobList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": [jobList.json() for job in jobList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no jobs."
        }
    ), 404

# add record
@app.route("/book/<string:jobID>",methods = ["POST"])
def addJob(jobID):
    book = Job.query.filter_by(jobID=jobID).first()
    if book:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "jobID":jobID
                },
                "message": "Job exist"
            }
        ), 400
    data = request.get_json()
    job = Job(jobID,**data)

    try:
        db.session.add(job)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "jobID": jobID
                },
                "message": "An error occurred posting the job."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": job.json()
        }
    ), 201






if __name__ == "__main__":
    app.run(port = 5000,debug = True)