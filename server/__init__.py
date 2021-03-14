from flask import Flask, request
import json, datetime

app = Flask(__name__, static_folder='../client', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')


# return JSON case file
@app.route('/api/cases', methods=["GET"])
def send_cases():
    with open('./client/cases/test.JSON') as f:
        case = json.load(f)
    return json.dumps(case)

# Processing cases
@app.route('/api/cases/filter', methods=["GET"])
def process_filter():
    result = ''
    ageRange = request.args.get('ageRange')
    startTime = request.args.get('startTime')
    endTime = request.args.get('endTime')
    gender = request.args.get('gender')

    #age
    if(ageRange != None):
        result += "Ages Range %s \n" % (ageRange)

    #date
    if(startTime != None and request.args.get('endTime') != None): 
        processedStart = datetime.datetime.fromisoformat(startTime[:-1])
        processedEnd = datetime.datetime.fromisoformat(endTime[:-1])
        result += "Time " + str(processedStart) + " to " + str(processedEnd) + "\n"

    #gender
    if(gender != None):
        result += "gender " + gender + "\n"

    return result

# return JSON case file
@app.route('/api/vaccine', methods=["GET"])
def send_vaccine():
    with open('./client/cases/test.JSON') as f:
        vaccine = json.load(f)
    return json.dumps(vaccine)

@app.route('/api/vaccine/filter', methods=["GET"])
def filter_vaccine():
    dateA = request.args.get('dateA')
    dateB = request.args.get('dateB')
    dateTimeA = datetime.datetime.fromisoformat(dateA[:-1])
    dateTimeB = datetime.datetime.fromisoformat(dateB[:-1])  
    return "Date " + str(dateTimeA) + " to " + str(dateTimeB) + "\n"