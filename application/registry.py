import os
from thingstance import Thing
from thingstance.stores.mongodb import MongoStore

database = "thingstance"

registers = {}


class Register(Thing):
    def __init__(self, name, *args, **kwargs):
        collection = name.lower()
        self._store = MongoStore(database=database, collection=collection)
        registers[collection] = self
        Thing.__init__(self, name=name, *args, **kwargs)

    # TBD: move to thingstance store / representations
    def load(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:

                # assumes one thing per-file. There may be many, eg CSV
                path = os.path.join(root, file)
                print("opening %s" % path)
                text = open(path).read()

                thing = Thing()

                # this belong in representation / thing
                suffix = os.path.splitext(path)[1]
                if suffix == ".yaml":
                    thing.yaml = text
                elif suffix == ".json":
                    thing.json = text

                self._store.put(thing)


# TBD: load registers from the register register
for name in ['Register',
             'Court',
             'School',
             'Datatype',
             'Field',
             'Instrument',
             'Measurement']:
    Register(name)
