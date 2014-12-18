import os
import ast
import json

from thing import Thing

class ThingLoader(object):

   def __init__(self, data_path, mongo):
      self.data_path = data_path
      self.mongo = mongo

   def load_json(self):
      data_dir = os.path.abspath(self.data_path)
      data_files = os.listdir(data_dir)
      for file in data_files:
         with open(os.path.join(data_dir, file)) as f:
            json_data = json.load(f)
            thing_list = []
            for d in json_data:
               thing = Thing(d)
               thing_list.append(thing.to_primitive())
            print("Loaded: %s" % file)
            self.mongo.db.things.insert(thing_list)
