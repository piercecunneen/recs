import json
import os

class Config(object):

  def __init__(self, isProduction):
    self.options = self.getCommonConfig()
    if isProduction:
      self.getProductionConfig()
    else:
      self.getDevelopmentConfig()

  def getCommonConfig(self):
    with open(os.path.join(os.path.dirname(__file__),'./common.json')) as f:
      return json.load(f)

  def getProductionConfig(self):
    with open(os.path.join(os.path.dirname(__file__),'./production.json')) as f:
      self.options.update(json.load(f))

  def getDevelopmentConfig(self):
    with open(os.path.join(os.path.dirname(__file__),'./development.json')) as f:
      self.options.update(json.load(f))
