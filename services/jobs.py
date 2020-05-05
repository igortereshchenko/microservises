from flask import Flask
from flask import request
from services.helpers import nice_json

import json

app = Flask(__name__)

with open("../database/jobs.json","r") as f:
    jobs = json.load(f)




@app.route("/", methods=['GET'])
def hello():
    return nice_json(
        {
            "uri": "/",
            "sub_uri":{
                        "jobs": "/jobs",
                        "user_jobs": "/jobs/<username>",
                        }
        }
    )

@app.route("/jobs/<username>", methods=['GET'])
def user_jobs(username):

    if username not in jobs:
        raise Exception('Not found')

    result = jobs[username]

    return nice_json(result)


@app.route("/jobs", methods=['GET'])
def jobs_info():
    return nice_json(jobs)




if __name__ =="__main__":
    app.run(port=5003, debug=True)