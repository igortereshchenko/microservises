from flask import  make_response
import json

def nice_json(info):
    response = make_response(json.dumps(info, sort_keys=True, indent=4))
    response.headers['Content-type'] = 'application/json'

    return response
