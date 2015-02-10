import os
from thingstance import Thing
from thingstance.stores.mongodb import MongoStore

registers = {}


class Register(Thing):
    def __init__(self, name, mongo_uri, *args, **kwargs):
        collection = name.lower()
        self._store = MongoStore(mongo_uri, collection=collection)
        registers[collection] = self
        Thing.__init__(self, name=name, *args, **kwargs)

    # TBD: move to thingstance store / representations
    def load(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:

                path = os.path.join(root, file)
                suffix = os.path.splitext(path)[1]

                # this belong in representation / thing

                # file of many things ..
                import csv
                with open(path) as f:
                    reader = csv.DictReader(f, delimiter='\t')
                    for d in reader:
                        if len(d.keys()):
                            thing = Thing()
                            thing.primitive = d
                            self._store.put(thing)

                # assumes one thing per-file.
                print("slurping %s" % path)
                text = open(path).read()

                thing = Thing()
                if suffix == ".yaml":
                    thing.yaml = text
                elif suffix == ".json":
                    thing.json = text

                self._store.put(thing)


# TBD: load registers from the register register
# for name in ['Register',
#              'Court',
#              'School',
#              'Datatype',
#              'Field',
#              'Instrument',
#              'Measurement']:
#     Register(name, app.config['MONGO_URI'])
