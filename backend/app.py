import re
from bson import ObjectId
from datetime import date, datetime, timedelta
from flask import Flask, request, session, jsonify
from pymongo import MongoClient, ReturnDocument
import bcrypt
import base64
from urllib.parse import urlparse, parse_qs
import statistics
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = "testing"

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.get_database("Test")
UserRecords = db.register
Applications = db.Applications
CareerFair = db.CareerFair
UserProfiles = db.Profiles


sender_address = 'develop.nak@gmail.com'
sender_pass =  'eyujkirliswosoag'

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)

# Route for registering a new user
@app.route("/register", methods=["post"])
def register():
    '''Gets input for registering a new user'''
    try:
        req = request.get_json()
        name = {"firstName": req["firstName"], "lastName": req["lastName"]}
        email = req["email"]
        passwordBase64 = req["password"]
        confirmPasswordBase64 = req["confirmPassword"]

        password = base64.b64decode(passwordBase64).decode('utf-8')
        confirmPassword = base64.b64decode(confirmPasswordBase64).decode('utf-8')

        '''Checks if email record already exists'''
        email_found = UserRecords.find_one({"email": email})
        if email_found:
            return jsonify({'error': "This email already exists in database"}), 400
        if password != confirmPassword:
            return jsonify({'error': "Passwords should match!"}), 400
        
        else:
            hashed = bcrypt.hashpw(confirmPassword.encode("utf-8"), bcrypt.gensalt())
            user_input = {"name": name, "email": email, "password": hashed}
            UserRecords.insert_one(user_input)
            
            '''find the new created account and its email'''
            # user_data = UserRecords.find_one({"email": email})
            # new_email = user_data["email"]
            '''if registered redirect to logged in as the registered user'''
            # session["email"] = new_email
            return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400


# Route for log in
@app.route("/login", methods=["POST"])
def login():
    ''' Gets login credentials from user '''
    try:
        req = request.get_json()
        email = req["email"]
        passwordBase64 = req["password"]
        password = base64.b64decode(passwordBase64).decode('utf-8')

        '''checks if email exists in database'''
        email_found = UserRecords.find_one({"email": email})
        if email_found:
            # email_val = email_found["email"]
            passwordcheck = email_found["password"]
            '''encode the password and check if it matches'''
            if bcrypt.checkpw(password.encode("utf-8"), passwordcheck):
                # session["email"] = email_val
                return jsonify({'message': 'Login successful'}), 200
            else:
                if "email" in session:
                    return jsonify({'message': 'Login successful'}), 200
                return jsonify({'error': "Wrong password"}), 400
        else:
            return jsonify({'error': "Email not found"}), 400
    except Exception as e:
        #print(e)
        return jsonify({'error': "Something went wrong"}), 400
# @app.route("/upload, methods = ["POST"])
#     def upload():
         # upload code goes here
#Route for logging out
@app.route("/logout", methods=["POST", "GET"])
def logout():
    '''Logs out current user'''
    '''if "email" in session:'''
    #     session.pop("email", None)
    return jsonify({'message': 'Logout successful'}), 200

def filterResults(applications, filter):
    ''' Applies filters for getting the desired records'''
    filteredApplications = []
    for application in applications:
        if( (application['companyName'].lower().find(filter.lower()) != -1) or (application['jobTitle'].lower().find(filter.lower()) != -1) or (application['jobId'].lower().find(filter.lower()) != -1) or (application['description'].lower().find(filter.lower()) != -1) or (application['url'].lower().find(filter.lower()) != -1) ):
            filteredApplications.append(application)
    return filteredApplications

@app.route("/view_applications", methods=["GET"])
def view_applications():
    try:
        '''Gets current user inputs'''
        '''if "email" in session:'''
        if request:
            # filtered_applications_list = lcache.get(str(request))
            # if filtered_applications_list != -1:
            #     return jsonify({'message': 'Applications found', 'applications': filtered_applications_list}), 200
            # email = session["email"]
            email = request.args.get("email")
            sort = request.args.get("sort")
            asc = 1 if request.args.get("asc") == "true" else -1
            filterString = request.args.get("filter")
            if(filterString is None) :
                filterString = ""
            pageNumber = int(request.args.get("page")) - 1
            print("email" + email)
            outapp = Applications.find({"email": email, 'status': 'applied'}).sort(sort, asc).skip(pageNumber*5).limit(5)
            outappList = []
            if outapp:
                for i in outapp:
                    outappList.append(i)

            outinr = Applications.find({"email": email, 'status': 'inReview'}).sort(sort, asc).skip(pageNumber*5).limit(5)
            outinrList = []
            if outinr:
                for i in outinr:
                    outinrList.append(i)

            outacc = Applications.find({"email": email, 'status': 'accepted'}).sort(sort, asc).skip(pageNumber*5).limit(5)
            outaccList = []
            if outacc:
                for i in outacc:
                    outaccList.append(i)

            outrej = Applications.find({"email": email, 'status': 'rejected'}).sort(sort, asc).skip(pageNumber*5).limit(5)
            outrejList = []
            if outrej:
                for i in outrej:
                    outrejList.append(i)

            outint = Applications.find({"email": email, 'status': 'interview'}).sort(sort, asc).skip(pageNumber*5).limit(5)
            outintList = []
            if outint:
                for i in outint:
                    outintList.append(i)
            out = outappList +  outinrList + outaccList + outintList + outrejList
            if out:
                applications_list = []
                # payload["msg"]="Applications present"
                for i in out:
                    del i['email']
                    i['_id']=str(i['_id'])
                    try:
                        i['reminder'] = i['reminder'].split('T')[0]
                    except: 
                        print("no reminders yet logged")
                    try:
                        i['interview'] = i['interview'].split('T')[0]
                    except: 
                        print("no interviews yet logged")

                    applications_list.append(i)
                filtered_applications_list = filterResults(applications_list, filterString)
                # lcache.put(str(request), filtered_applications_list)
                return jsonify({'message': 'Applications found', 'applications': filtered_applications_list}), 200
            else:
                return jsonify({'message': 'You have no applications', 'applications': []}), 200
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400
            
    except Exception as e:
        #print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/add_application", methods=["POST"])
def add_application():
    '''Route for adding application'''
    try:
        '''if "email" in session:'''
        if request:
            req = request.get_json()
            print(request.args)
            try:
                description = req["description"]
            except:
                description = ""
            try:
                date = req["date"]
            except:
                date = ""
            application = {
                "email": req["email"],
                "companyName": req["companyName"],
                "jobTitle": req["jobTitle"],
                "jobId": req["jobId"],
                "description": description,
                "url": req["url"],
                "date": date,
                "status": req["status"], 
                "contact": "Contact Details: "
            }
            print("dd", application)
            try:
                Applications.insert_one(application)
                return jsonify({"message": "Application added successfully"}),200
            except Exception as e:
                return jsonify({"error": "Unable to add Application"}),400
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/delete_application", methods=["POST"])
def delete_application():
    ''' Route for deleting an application'''
    try:
        '''if "email" in session:'''
        if request:
            req = request.get_json()
            email = req["email"]
            _id = req["_id"]
            # delete_document = Applications.find_one_and_delete({"_id":jobId, "email":email})
            delete_document = Applications.find_one_and_delete({"_id":ObjectId(_id), "email":email})
            if delete_document == None:
                return jsonify({"error": "No such Job ID found for this user's email"}), 400
            else:
                return jsonify({"message": "Job Application deleted successfully"}), 200
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/change_status", methods=["POST"])
def change_status():
    '''Route for changing the status of an application'''
    try:
        '''if "email" in session:'''
        if request:
            req = request.get_json()
            email = req["email"]
            _id = req["_id"]
            filter = {'_id':ObjectId(_id), "email": email}

            application = {
                "status": req["status"]
            }
            set_values = {"$set": application}
            modify_document = Applications.find_one_and_update(filter, set_values, return_document = ReturnDocument.AFTER)
            if modify_document == None:
                return jsonify({"error": "No such Job ID found for this user's email"}), 400
            else:
                return jsonify({"message": "Job Application modified successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400


@app.route("/add_contact_details", methods=["POST"])
def add_contact_details():
    '''Route for adding the contact details of a user'''
    try:
        ''' if "email" in session:'''
        if request:
            req = request.get_json()
            email = req["email"]
            _id = req["_id"]
            filter = {'_id':ObjectId(_id), "email": email}
            print(req)
            application = {
                "contact": req["contactName"],
                "reminder" : req["reminder"]
            }
            set_values = {"$set": application}
            modify_document = Applications.find_one_and_update(filter, set_values, return_document = ReturnDocument.AFTER)
            if modify_document == None:
                return jsonify({"error": "No such Job ID found for this user's email"}), 400
            else:
                return jsonify({"message": "Job Application modified successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/modify_application", methods=["POST"])
def modify_application():
    '''Route for modifying an application'''
    try:
        # if "email" in session:
        if request:
            req = request.get_json()
            print(req)
            email = req["email"]
            _id = req["_id"]
            filter = {'_id':ObjectId(_id), "email": email}
            # filter = {"_id": jobId, "email": email}

            application = {
                "email": req["email"],
                "companyName": req["companyName"],
                "jobTitle": req["jobTitle"],
                "jobId": req["jobId"],
                "description": req["description"],
                "url": req["url"],
                "date": req["date"],
                "status": req["status"]
            }
            set_values = {"$set": application}
            modify_document = Applications.find_one_and_update(filter, set_values, return_document = ReturnDocument.AFTER)
            if modify_document == None:
                return jsonify({"error": "No such Job ID found for this user's email"}), 400
            else:
                return jsonify({"message": "Job Application modified successfully"}), 200
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400
    
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/next_stage_application", methods=["POST"])
def next_stage_application():
    '''Route for moving the application to the next stage'''
    try:
        '''if "email" in session:'''
        if request:
            req = request.get_json()
            email = req["email"]
            _id = req["_id"]
            filter = {'_id':ObjectId(_id), "email": email}
            if req['status'] == 'applied': 
                req['status'] = 'interview'
            # filter = {"_id": jobId, "email": email}
            print(req)
            application = {
                "email": req["email"],
                "description": req["description"],
                "reminder": req["reminder"],
                "interview": req["interview"],
                "status": req["status"]
            }
            set_values = {"$set": application}
            '''Updates the stage of the application'''
            modify_document = Applications.find_one_and_update(filter, set_values, return_document = ReturnDocument.AFTER)
            if modify_document == None:
                return jsonify({"error": "No such Job ID found for this user's email"}), 400
            else:
                return jsonify({"message": "Job Application modified successfully"}), 200
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400
    
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/add_career_fair", methods=["POST"])
def add_career_fair():
    '''Route for adding career fair'''
    try:
        '''if "email" in session:'''
        if request:
            req = request.get_json()
            try:
                description = req["description"]
            except:
                description = ""
            try:
                date = req["date"]
            except:
                date = ""
            print(req)
            '''Sets attributes of career fair'''
            career_fair = {
                "email": req["email"],
                "careerFairName": req["careerFairName"],
                "description": description,
                "url": req["url"],
                "date": date,
            }
            try:
                '''Adds a career fair'''
                CareerFair.insert_one(career_fair)
                return jsonify({"message": "Application added successfully"}),200
            except Exception as e:
                #print(str(e))
                return jsonify({"error": "Unable to add Application"}),400
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/view_careerfairs", methods=["GET"])
def view_careerfairs():
    '''Route for viewing career fairs'''
    try:
        '''if "email" in session:'''
        if request:
            # email = session["email"]
            email = request.args.get("email")
#            sort = request.args.get("sort")
#            asc = 1 if request.args.get("asc") == "true" else -1
            out = CareerFair.find({"email": email})#.sort(sort, asc)
            if out:
                careerfair_list = []
                # payload["msg"]="Applications present"
                for i in out:
                    del i['email']
                    i['_id']=str(i['_id'])
                    i['date'] = i['date'].split('T')[0]
                    careerfair_list.append(i)
                return jsonify({'message': 'Applications found', 'applications': careerfair_list}), 200
            else:
                return jsonify({'message': 'You have no career fairs added'}), 200
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400
            
    except Exception as e:
        #print(e)
        return jsonify({'error': "Something went wrong"}), 400

# Route for creating profile
@app.route("/create_profile", methods=["post"])
def create_profile():
    try:
        '''if "email" in session:'''
        if request:
            req = request.get_json()
            email = req["email"]
            '''Checks if user profile already exists'''
            email_found = UserProfiles.find_one({"email": email})
            if email_found:
                return jsonify({"error": "Profile already created."}),400
            else:
                user_profile = {
                    "firstName": req["firstName"],
                    "lastName": req["lastName"],
                    "email": req["email"], 
                    "phone": req.get("phone"),
                    "city": req.get("city"),
                    "state": req.get("state"),
                    "resume": req.get("resume"),
                    "gitHub": req.get("gitHub"),
                    "linkedIn": req.get("linkedin"),
                    "skills": req.get("skills", '').split(","),
                    "about": req.get("about"),
                    "interests": req.get("interests", '').split(","),
                    "companyName": req.get("companyName"),
                    "jobTitle": req.get("jobTitle"),
                    "description": req.get("description"),
                    "jobCity": req.get("jobCity"),
                    "jobState": req.get("jobState"),
                    "jobFrom": req.get("jobDate"),
                    "toFrom": req.get("jobDate"),
                    "curentJob": req.get("curentJob"),
                    "institution": req.get("institution"),
                    "major": req.get("major"),
                    "degree": req.get("degree"),
                    "courses": req.get("courses", '').split(","),
                    "universityCity": req.get("universityCity"),
                    "universityState": req.get("universityState"),
                    "universityFromDate": req.get("universityDate"),
                    "universityToDate": req.get("universityDate"),
                    "curentUniversity": req.get("curentUniversity")
                }
                try:
                    '''Creates a profile for the user'''
                    UserProfiles.insert_one(user_profile)
                    return jsonify({"message": "Profile created successfully"}),200
                except Exception as e:
                    return jsonify({"error": "Unable to create profile"}),400
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/view_profile", methods=["GET"])
def view_profile():
    '''Route for viewing profile'''
    try:
        '''if "email" in session:'''
        if request:
            email = request.args.get("email")
            filter = {"email": email}
            '''Gets the profile'''
            profile = UserProfiles.find(filter)
            if profile == None:
                return jsonify({'message': "Create a profile first", "profile": {}}), 200
            else:
                # payload["profile"] = profile
                profile_out = {}
                for p in profile:
                    p['_id'] = str(p['_id'])
                    profile_out = p
                return jsonify({'message': "Found User Profile", "profile": profile_out}), 200
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

# route for getting statistics
@app.route("/get_statistics", methods=["GET"])
def get_statistics():
    try:
        '''if "email" in session:'''
        if request:
            email = request.args.get("email")
            filter = {"email": email}
            '''finds the profile and application details for a users statistics page''' 
            profile = UserProfiles.find(filter)
            app = Applications.find({"email": email})
            career = CareerFair.find({"email": email})
            if profile == None:
                return jsonify({'message': "Create a profile first", "profile": {}}), 200
            else:
                if app:
                    applications_list = []
                    for i in app:
                        del i['email']
                        i['_id']=str(i['_id'])
                        applications_list.append(i)

                    careerfair_list = []
                    for i in career:
                        del i['email']
                        i['_id']=str(i['_id'])
                        i['date'] = i['date'].split('T')[0]
                        careerfair_list.append(i)

                '''built a plotly dashboard based on the profile and applications for the user '''
                json = statistics.build_dashboard(applications_list, careerfair_list)
                return json
                
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/get_statistics_indicators", methods=["GET"])
def get_statistics_indicators():
    try:
        '''if "email" in session:'''
        if request:
            email = request.args.get("email")
            filter = {"email": email}
            '''finds the profile and application details for a users statistics page '''
            profile = UserProfiles.find(filter)
            app = Applications.find()
            career = CareerFair.find()
            if profile == None:
                return jsonify({'message': "Create a profile first", "profile": {}}), 200
            else:
                if app:
                    applications_list = []
                    for i in app:
                        i['_id']=str(i['_id'])
                        applications_list.append(i)

                if career: 
                    careerfair_list = []
                    for i in career:
                        i['_id']=str(i['_id'])
                        i['date'] = i['date'].split('T')[0]
                        careerfair_list.append(i)

                '''built a plotly dashboard based on the profile and applications for the user''' 
                json = statistics.build_indicators(applications_list, careerfair_list, email)
                return json

    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

@app.route("/modify_profile", methods=["POST"])
def modify_profile(): 
    try:
        '''if "email" in session:'''
        if request:
            req = request.get_json()
            _id = req["_id"]
            email = req["email"]
            email_found = UserProfiles.find_one({"_id": ObjectId(_id), "email": email})
            if not email_found:
                return jsonify({"error": "Profile not found."}),400
            else:
                user_profile = {
                    "firstName": req["firstName"],
                    "lastName": req["lastName"],
                    "email": req["email"], 
                    "phone": req.get("phone"),
                    "city": req.get("city"),
                    "state": req.get("state"),
                    "resume": req.get("resume"),
                    "gitHub": req.get("gitHub"),
                    "linkedIn": req.get("linkedin"),
                    "skills": req.get("skills", '').split(","),
                    "about": req.get("about"),
                    "interests": req.get("interests", '').split(","),
                    "companyName": req.get("companyName"),
                    "jobTitle": req.get("jobTitle"),
                    "description": req.get("description"),
                    "jobCity": req.get("jobCity"),
                    "jobState": req.get("jobState"),
                    "jobFrom": req.get("jobDate"),
                    "toFrom": req.get("jobDate"),
                    "curentJob": req.get("curentJob"),
                    "institution": req.get("institution"),
                    "major": req.get("major"),
                    "degree": req.get("degree"),
                    "courses": req.get("courses", '').split(","),
                    "universityCity": req.get("universityCity"),
                    "universityState": req.get("universityState"),
                    "universityFromDate": req.get("universityDate"),
                    "universityToDate": req.get("universityDate"),
                    "curentUniversity": req.get("curentUniversity")
                }

                set_values = {"$set":user_profile}
                filter = {"email": email}
                '''Updates the profile'''
                modify_document = UserProfiles.find_one_and_update(filter, set_values, return_document = ReturnDocument.AFTER)
                if modify_document == None:
                    return jsonify({"error": "Unable to modify profile"}),400
                else:
                    return jsonify({"message": "Profile modified successfully"}),200    
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400    

# Route for clearing up a profile
@app.route("/clear_profile", methods=["POST"])
def clear_profile():
    '''if "email" in session:'''
    try:
        if request:
            req = request.get_json()
            email_to_delete = req["email"]
            _id = req["_id"]
            delete_user = UserRecords.find_one({"email":email_to_delete})
            if delete_user == None:
                return jsonify({'error': "User email not found"}), 400
            '''Deletes the profile'''
            delete_profile = UserProfiles.find_one_and_delete({"_id": ObjectId(_id), "email":email_to_delete})
            if delete_profile == None:
                return jsonify({'error': "Profile not found"}), 400
            else:
                return jsonify({"message": "User Profile cleared successfully"}), 200
        # else:
        #     return jsonify({'error': "Not Logged in"}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

# Route for getting upcoming interview dates
@app.route("/interviews", methods=["get"])
def interviews() :
    '''if "email" in session:'''
    try:
        if request:
            email = request.args.get("email")
            today = str(datetime.today()).split()[0]
            query = {"email": email, "interview": {"$gte": today}}
            projection = {"date":1, "_id":0, "companyName": 1, "jobTitle": 1}
            '''Gets records that have upcoming interviews scheduled'''
            item_details = Applications.find(query,projection)
            if item_details == None:
                return jsonify({"error": "No such Job ID found for this user's email"})
            else: 
                return jsonify(list(item_details))
    except Exception as e:
        print(e)
        return jsonify({'error': "Something went wrong"}), 400

def send_reminders():
    '''For sending automated reminder emails to users'''
    current_date = datetime.now.strftime("%Y-%m-%d")      
    records = Applications.find({"date":{"$regex":"^"+current_date}})
    for record in records:
        receiver_address = record['email']
       
        message = MIMEMultipart()

        message['Subject'] = 'This is a Reminder for your Interview at '+record['companyName'] 
        mail_content = '''Hello,
        This is a reminder email about your interview for the role '''+record["jobTitle"]+' at '+record['companyName'] + ' on ' + record['date']
       
        message['From'] = sender_address
        message['To'] = receiver_address

        message.attach(MIMEText(mail_content, 'plain'))

        try:
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()

        except Exception as e: 
            print("Failed to send a reminder, the err: ", e)


if __name__ == "__main__":
  sched = BackgroundScheduler(daemon=True)
  sched.add_job(send_reminders, 'cron', day='*', hour='5')
  sched.start()
#   lcache = LRUCache(100)
  app.run(debug=True, host="0.0.0.0", port=8000, threaded=True)
