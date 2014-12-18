import math
import re

from thing import Thing
from bson.objectid import ObjectId


class Repository(object):

    def __init__(self, mongo):
        self.mongo = mongo

    def save_thing(self, thing):
        return self.mongo.db.things.insert(thing.to_primitive())

    def find_types(self):
        cursor = self.mongo.db.things.distinct('type')
        types = [{"type" : type} for type in cursor]
        return types

    def find_thing_by_id(self, type, _id):
        thing = self.mongo.db.things.find_one({'_id' : ObjectId(_id), 'type' : re.compile(type, re.IGNORECASE)})
        return Thing(thing)

    def find_thing_by_uid(self, type, uid):
        thing = self.mongo.db.things.find_one({'uid' : uid, 'type' : re.compile(type, re.IGNORECASE)})
        return Thing(thing)

    def find_thing_by_owner(self, type, owner):
        results = self.mongo.db.things.find({'fields.issuedFor' : owner})
        things = [Thing(thing).to_primitive() for thing in results]
        return things

    def find_things_by_type(self, type, page, page_size):
        total = self.mongo.db.things.find({'type' : type}).count()
        pages = math.ceil(total/page_size)
        if page == 1:
            start = page - 1
        else:
            start = (page - 1) * page_size

        cursor = self.mongo.db.things.find({'type' : re.compile(type, re.IGNORECASE)})[start : start+page_size]

        things = [Thing(thing).to_primitive() for thing in cursor]

        results = { "meta" :
                        {   "type" : type,
                            "page" : page,
                            "total_pages ": pages,
                            "total_results" : total,
                            "results_this_page" : len(things)
                        },
                    type : things
                }
        return results
