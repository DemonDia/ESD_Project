from flask import Flask, request, jsonify
import json
import pyrebase as pb

from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app)

# app.config['CORS_HEADERS'] = 'Content-Type'


firebaseConfig = {
  "apiKey": "AIzaSyCCD_YMl1GVhCacEWtj424cMrmqHWqyzw0",
  "authDomain": "jobmicroservice-13a0c.firebaseapp.com",
  "databaseURL": "https://jobmicroservice-13a0c-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "jobmicroservice-13a0c",
  "storageBucket": "jobmicroservice-13a0c.appspot.com",
  "messagingSenderId": "209394015065",
  "appId": "1:209394015065:web:b6612fd69caeaea6124a48"
}

firebase = pb.initialize_app(firebaseConfig)
auth = firebase.auth() #use authentication
db = firebase.database() #user realtime db
auth.current_user = None

@app.route("/users")
def getUsers():
    try:
        users = db.child("users").get()
        userDict = {}        
                
    
        for user in users.each():
            print(type(user.key()))
            print("___________") 
            print("key:",user.key())
            print("value:",user.val())
            userDict[user.key()] = user.val()
        # return userDict
        return json.dumps(userDict) #return all user data
    except Exception as e:
        print(e)
        return "NOT OK"

@app.route("/login",methods = ["POST"])
def login():
    try:
        data = request.data.decode("utf-8") #decode bytes 
        data = json.loads(data)
        email = data["loginEmail"] #variable from the react UI
        password = data["loginPassword"] #variable from react UI
        auth.sign_in_with_email_and_password(email,password)
    
        # print("HHHA")
        return "OK"
    except:
        # print("Invalid email and/or password!")
        return "NOT OK"


@app.route("/user/<string:email>")
def findByEmail(email):
    try:
        userDict = {}
        user = db.child("users").order_by_child("email").equal_to(email).get()
        userDict[user.key()] = user.val()
        print(userDict["users"])
        # print(user.key())
        print(bool(userDict["users"])) #return true and false

# bool(userDict["users"])

        if(bool(userDict["users"])): #yes theres an existing user
            return json.dumps(userDict)
        else:
            return "404"  #empty user valu
    # print(userDict.values())
    # print(type(user))
    #     # pass
    except Exception as e:
        print(e)
        return "NOT OK"

@app.route("/user/add_education/<string:email>",methods = ["POST"])
def addEducation(email):
    # try:
    userDict = {}
    user = db.child("users").order_by_child("email").equal_to(email).get()
    print(user)
    user_id = user.key()
    userDict[user.key()] = user.val()
    for user_result in user.each():
        user_id = user_result.key()
        # print(user.key()) 
    # print(user.val())
    # print(userDict["users"])
    # print(user.key())
    print(bool(userDict["users"]))
    if(bool(userDict["users"])):
        
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data)
        print(data)
        path = "users/{0}/{1}/education".format(user_id,email)
        print(path)
        # print("users/{0}/{1}/education".format(user_id,email))
        db.child(path).push(data)
        # user.child("education").push(data)
        # add skill
        return "OK"
    else:
        return "404" 
    # print(userDict.values())
    # print(type(user))
    #     # pass
    # except:
    #     return "NOT OK"

@app.route("/register",methods = ["POST"])
# @cross_origin()
def register():
    try:
        data = request.data.decode("utf-8") #decode bytes --> data received is in bytes; need to decode 
        data = json.loads(data)
        print(data)
        email = data["email"]
        password = data["password"]
        cfmpassword = data["registerConfirmPassword"]
        print(cfmpassword == password)
        if(cfmpassword == password):
            #remove password from the json data;
            #we are not saving passwords in the realtime database for security reasons
            del data['password']
            del data['registerConfirmPassword']

            #create user account in the authentication part
            auth.create_user_with_email_and_password(email,password)
            #add record into realtime database
            db.child("users").push(data)
            return "OK"
        else:
            print("GG")
            return "NOT OK"
        
    except Exception as e:
        print(e)
        return "NOT OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 5007,debug = True)