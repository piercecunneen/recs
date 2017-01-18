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

import logging
from scripts import validate

CONFIG = Config(False)
app = Flask(__name__) # pylint: disable=invalid-name

with open("./resources/api-validation.json", "r") as f:
  api_validation = json.load(f) # pylint: disable=invalid-name

bad_request = {  # pylint: disable=invalid-name
  "error": "bad request"
}

good_request = { # pylint: disable=invalid-name

}

@app.route("/api/v1.0/", methods=["GET", "OPTIONS"])
def api_root():
  """
    base url for the backend api
  """
  logging.info("THIS IS A TEST")
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
      return jsonify(good_request)
    else:
      return result

  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/user_favorites/<user_id>/", methods=["GET", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def get_user_favorites(user_id):
  """
    returns all the favorites associated with a user
  """

  try:
    user_id = int(user_id)
  except ValueError:
    return jsonify(bad_request)
  favorites = fav_db.get_user_favorites(user_id)
  favorites_obj = {
    'favorites': []
  }
  if isinstance(favorites, tuple):
    favorites_obj = {
      'favorites': []
    }
    
    for fav in favorites:
      fav_item = {
        'user_id': fav[0],
        'item_id': fav[1],
        'item_type': fav[2],
        'time_favorited': fav[3],
        'item_data':  json.loads(fav[5])
      }
      favorites_obj['favorites'].append(fav_item)
    return jsonify(favorites_obj)
  else:
    return jsonify(favorites_obj)

@app.route("/api/v1.0/user_recommendations/<user_id>/", methods=["GET", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def get_user_recommendations(user_id):
  """
    returns all the recommendations associated with a user
  """

  try:
    user_id = int(user_id)
  except ValueError:
    return jsonify(bad_request)
  recommendations = rec_db.get_user_recommendations(user_id)
  recommendations_obj = {
    'recommendations': []
  }
  if isinstance(recommendations, tuple):
    for rec in recommendations:
      rec_item = {
        'rec_id':             rec[0],
        'from_user_id':       rec[1],
        'to_user_id':         rec[2],
        'item_id':            rec[3],
        'time_recommended':   rec[5],
        'rating':             rec[6],
        'item_data':          json.loads(rec[9])
      }
      recommendations_obj['recommendations'].append(rec_item)
    return jsonify(recommendations_obj)
  else:
    return jsonify(recommendations_obj)

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
        return jsonify(good_request)
      else:
        return result

    else:
      logging.info("ERROR")
      logging.info(request_body)
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
      return jsonify(good_request)
    else:
      return result

  else:
    logging.info("ERROR")
    logging.info(request_body)
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
      return jsonify(good_request)
    else:
      return result

  else:
    logging.info("ERROR")
    logging.info(api_validation['add_favorite'])
    logging.info(request_body)
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
      return jsonify(good_request)
    else:
      return result

  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/albums_recommendation_data/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def albums_recommendation_data():
  """
    get album recommendation data (album and tracks)
  """
  request_body = request.json
  validation = validate.validate_request(
    api_validation['albums_recommendation_data'],
    request_body
  )
  if validation:
    albums = {}
    for album in request_body['albums']:
      album_id = album['album_id']
      albums[album_id] = rec_db.get_album_rec_data(album)
    if not albums:
      return jsonify({})
    else:
      albums_filtered = {}
      for album_id in albums:
        relevant_results = [
          {
            'from_user_id':    row[1],
            'item_id': row[3]
          }
          for row  in albums[album_id]
        ]
        album_filtered = {}
        for row in relevant_results:
          item_id = row['item_id']
          if album_filtered.get(item_id):
            album_filtered[item_id]['items'].append([row['from_user_id']])
            album_filtered[item_id]['count'] += 1
          else:
            album_filtered[item_id] = {}
            album_filtered[item_id]['count'] = 1
            album_filtered[item_id]['items'] = [[row['from_user_id']]]
        albums_filtered[album_id] = album_filtered
      return jsonify(albums_filtered)
  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/albums_favorite_data/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def albums_favorite_data():
  """
    get album favorite data (album and tracks)
  """
  request_body = request.json
  validation = validate.validate_request(
    api_validation['albums_favorite_data'],
    request_body
  )
  if validation:
    albums = {}
    for album in request_body['albums']:
      album_id = album['album_id']
      albums[album_id] = fav_db.get_album_fav_data(album)
      print albums
    if not albums:
      return jsonify({})
    else:
      albums_filtered = {}
      for album_id in albums:
        relevant_results = [
          {
            'user_id':    row[0],
            'item_id':    row[1],
            'item_type':  row[2]
          }
          for row  in albums[album_id]
        ]
        album_filtered = {}
        for row in relevant_results:
          item_id = row['item_id']
          if album_filtered.get(item_id):
            album_filtered[item_id]['items'].append(
              {'user_id': row['user_id'], 'item_type': row['item_type']}
            )
            album_filtered[item_id]['count'] += 1
          else:
            album_filtered[item_id] = {}
            album_filtered[item_id]['count'] = 1
            album_filtered[item_id]['items'] = [
              {'user_id': row['user_id'], 'item_type': row['item_type']}
            ]
        albums_filtered[album_id] = album_filtered
      return jsonify(albums_filtered)
  else:
    return jsonify(bad_request)

@app.route("/api/v1.0/submit_rec_rating/", methods=["POST", "OPTIONS"])
@crossdomain(origin='*', headers='Content-Type')
def submit_rec_rating():
  """
    submit rating for a recommendation
  """
  request_body = request.json
  validation = validate.validate_request(
    api_validation['submit_rec_rating'],
    request_body
  )
  if validation:
    rec_db.add_rec_rating(request_body)
    return jsonify(good_request)
  else:
    return jsonify(bad_request)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=2323, debug=CONFIG.options['debug'], threaded=True)
