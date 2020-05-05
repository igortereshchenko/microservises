from flask import Flask
from flask import request
from services.helpers import nice_json

import json

app = Flask(__name__)

with open("../database/company.json","r") as f:
    companies = json.load(f)

# print(companies)


@app.route("/", methods=['GET'])
def hello():
    return nice_json(
        {
            "uri": "/",
            "sub_uri":{
                        "companies": "/companies",
                        "company": "/company/<id>",

                        }
        }
    )

@app.route("/company/<id>", methods=['GET'])
def company_info(id):

    if id not in companies:
        raise Exception('Not found')

    result = companies[id]
    result["uri"] = request.url

    return nice_json(result)


@app.route("/companies", methods=['GET'])
def companies_info():
    return nice_json(companies)


if __name__ =="__main__":
    app.run(port=5001, debug=True)