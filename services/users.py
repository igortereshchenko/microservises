from flask import Flask
from flask import request
from services.helpers import nice_json
import requests

import json

app = Flask(__name__)

with open("../database/users.json","r") as f:
    users = json.load(f)




@app.route("/", methods=['GET'])
def hello():
    return nice_json(
        {
            "uri": "/",
            "sub_uri":{
                        "users": "/users",
                        "user": "/user/<username>",
                        "jobs": "/user/<username>/jobs",
                        "suggested": "/user/<username>/suggestions",
                        }
        }
    )

@app.route("/user/<username>", methods=['GET'])
def user_info(username):

    if username not in users:
        raise Exception('Not found')

    result = users[username]

    return nice_json(result)


@app.route("/users", methods=['GET'])
def companies_info():
    return nice_json(users)


@app.route("/user/<username>/jobs", methods=['GET'])
def user_jobs(username):

    if username not in users:
        raise Exception('User not found')

    try:
        user_jobs= requests.get("http://127.0.0.1:5003/jobs/{}".format(username))
    except Exception as e: #check connection
        raise Exception("Job service is not unavailable")

    if user_jobs.status_code ==404:
        raise Exception("No jobs found")

    user_jobs = user_jobs.json()

    result = {}

    for date, jobs in user_jobs.items():
        result[date]=[]
        for company_id in jobs:

            try:
                company = requests.get("http://127.0.0.1:5001/company/{}".format(company_id))
            except Exception as e:
                raise Exception("Company service is not unavailable")


            if company.status_code == 404:
                raise Exception("No company found")

            company = company.json()

            result[date].append({
                "title":company["title"],
                "rating": company["rating"],
                "uri": company["uri"],
            })


    return nice_json(result)




@app.route("/user/<username>/suggestions", methods=['GET'])
def user_jobs_suggestions(username):
    raise NotImplementedError();


if __name__ =="__main__":
    app.run(port=5000, debug=True)