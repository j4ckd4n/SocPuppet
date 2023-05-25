import json

config = {}

def loadConfig(path):
  global config
  with open(path, 'r') as f:
    config = json.load(f)