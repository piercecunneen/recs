#!/usr/local/bin/python
from flask import Flask, jsonify
import os

from config.config import Config

config = Config(False)

app = Flask(__name__)

@app.route("/api/v1.0/", methods=["GET"])
def apiRoot():
    return jsonify({"key": "val"})



if __name__ == "__main__":
  app.run(port=9934, debug = config.options['debug'])