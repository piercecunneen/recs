"""
Entry into backend api
"""
import json
from flask import Flask, jsonify, request

from config.config import Config
from routing import crossdomain

# db functions
import src.db.users.create_user as  users
import src.db.requests.add_request as request_db
import src.db.recommendation.add_recommendation as recommendation_db


from scripts import validate

CONFIG = Config(False)
app = Flask(__name__) # pylint: disable=invalid-name

with open("./resources/api-validation.json", "r") as f:
  api_validation = json.load(f) # pylint: disable=invalid-name

bad_request = {  # pylint: disable=invalid-name
  "error": "bad request"
}

@app.route("/api/v1.0/", methods=["GET", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def api_root():
  """
    base url for the backend api
  """
  return jsonify({"key": "val"})

@app.route("/api/v1.0/create_user/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def create_user():
  """
    Sending a post request to this route will create a user account on backend
  """
  request_body = request.json
  validation = validate.validate_request(api_validation['create_user'], request_body)
  if validation:
    result = users.create_user(request_body)
    if not result:
      return "Good POST"
    else:
      return result

  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/add_request/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def add_request():
  """
    add (POST) a request for a recommendation
  """
  if request.method == "POST":
    request_body = request.json
    validation = validate.validate_request(api_validation['add_request'], request_body)
    if validation:
      result = request_db.add_request(request_body)
      if not result:
        return "Good POST"
      else:
        return result

    else:
      return jsonify(bad_request)


@app.route("/api/v1.0/add_recommendation/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def add_recommendation():
  """
    add (POST) a recommendation
  """
  if request.method == "POST":
    request_body = request.json
    validation = validate.validate_request(api_validation['add_recommendation'], request_body)
    if validation:
      result = recommendation_db.add_recommendation(request_body)
      if not result:
        return "Good POST"
      else:
        return result

    else:
      return jsonify(bad_request)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=2323, debug=CONFIG.options['debug'])

