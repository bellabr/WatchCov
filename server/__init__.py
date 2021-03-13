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

# process age request
@app.route('/api/cases/age', methods=["GET"])
def process_age():
    startAge = request.args.get('startAge')
    endAge = request.args.get('endAge')
    return "Ages %s to %s" % (startAge, endAge)

# process date request
@app.route('/api/cases/date', methods=["GET"])
def process_date():
    startTime = request.args.get('startTime')
    processedStart = datetime.datetime.fromisoformat(startTime[:-1])
    endTime = request.args.get('endTime')
    processedEnd = datetime.datetime.fromisoformat(endTime[:-1])
    return "Time " + str(processedStart) + " to " + str(processedEnd)