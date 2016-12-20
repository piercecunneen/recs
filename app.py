"""
Entry into backend api
"""
from flask import Flask, jsonify

from recs.config.config import Config

CONFIG = Config(False)
APP = Flask(__name__)

@APP.route("/api/v1.0/", methods=["GET"])
def api_root():
  """
    base url for the backend api
  """
  return jsonify({"key": "val"})

if __name__ == "__main__":
  APP.run(port=9934, debug=CONFIG.options['debug'])

