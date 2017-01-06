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
import src.db.recommendations as rec_db
import src.db.favorites as fav_db

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
    add a request for a recommendation
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
    add  a recommendation
  """
  request_body = request.json
  validation = validate.validate_request(api_validation['add_recommendation'], request_body)
  if validation:
    result = rec_db.add_rec(request_body)
    if not result:
      return "Good POST"
    else:
      return result

  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/add_favorite/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def add_favorite():
  """
    add  a recommendation
  """
  request_body = request.json
  validation = validate.validate_request(api_validation['add_favorite'], request_body)
  if validation:
    result = fav_db.add_fav(request_body)
    if not result:
      return "Good POST"
    else:
      return result

  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/remove_favorite/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def remove_favorite():
  """
    add  a recommendation
  """
  request_body = request.json
  validation = validate.validate_request(api_validation['remove_favorite'], request_body)
  if validation:
    result = fav_db.remove_fav(request_body)
    if not result:
      return "Good POST"
    else:
      return result

  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/get_album_recommendation_data/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def get_album_recommendation_data():
  """
    get album recommendation data (album and tracks)
  """
  request_body = request.json
  validation = validate.validate_request(
    api_validation['get_album_recommendation_data'],
    request_body
  )

  if validation:
    result = rec_db.get_album_rec_data(request_body)

    if not result:
      return jsonify({})
    else:

      relevant_results = [
        {
          'from_user_id':    row[1],
          'item_id': row[3]
        }
        for row  in result
      ]
      results_filtered = {}
      for row in relevant_results:
        item_id = row['item_id']
        if results_filtered.get(item_id):
          results_filtered[item_id]['items'].append([row['from_user_id']])
          results_filtered[item_id]['count'] += 1
        else:
          results_filtered[item_id] = {}
          results_filtered[item_id]['count'] = 1
          results_filtered[item_id]['items'] = [[row['from_user_id']]]
      return jsonify(results_filtered)
  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/get_album_favorite_data/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def get_album_favorite_data():
  """
    get album favorite data (album and tracks)
  """
  request_body = request.json
  validation = validate.validate_request(
    api_validation['get_album_favorite_data'],
    request_body
  )

  if validation:
    result = fav_db.get_album_fav_data(request_body)
    if not result:
      return jsonify({})
    else:

      relevant_results = [
        {
          'user_id':    row[0],
          'item_id':    row[1],
          'item_type':  row[2]
        }
        for row  in result
      ]
      results_filtered = {}
      for row in relevant_results:
        item_id = row['item_id']
        if results_filtered.get(item_id):
          results_filtered[item_id]['items'].append({'user_id': row['user_id'], 'item_type': row['item_type']})
          results_filtered[item_id]['count'] += 1
        else:
          results_filtered[item_id] = {}
          results_filtered[item_id]['count'] = 1
          results_filtered[item_id]['items'] = [{'user_id': row['user_id'], 'item_type': row['item_type']}]
      return jsonify(results_filtered)
  else:
    return jsonify(bad_request)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=2323, debug=CONFIG.options['debug'])



