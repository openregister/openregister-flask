import os
from thingstance import Thing
from thingstance.stores.mongodb import MongoStore

database = "thingstance"

repositories = {}


class Repository(Thing):
    def __init__(self, name, *args, **kwargs):
        collection = name.lower()
        self._store = MongoStore(database=database, collection=collection)
        repositories[collection] = self
        Thing.__init__(self, name=name, *args, **kwargs)

    # this belong in store / representations ..
    def load(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:

                # assumes one thing per-file. There may be many, eg CSV
                path = os.path.join(root, file)
                text = open(path).read()

                thing = Thing()

                # this belong in representation / thing
                suffix = os.path.splitext(path)[1]
                if suffix == ".yaml":
                    thing.yaml = text
                elif suffix == ".json":
                    thing.json = text

                self._store.put(thing)


# TBD URL scheme for registry/register/repository still unclear ..
Repository(name='Thingstance')
Repository(name='Datatype', registry='Types', registers=['Datatype'])
Repository(name='Field', registers=['Field'])
Repository(name='Tag', registers=['Tag'])
Repository(name='registry', registers=['Education', 'Organisation'])
Repository(name='Types', registers=['Datatype', 'Tag', 'Field'])
Repository(name='Education',
           registers=['School', 'Headteacher', 'Location', 'PostalAddress'])
Repository(name='Organisation')
Repository(name='Notice')
Repository(name='Geography')
