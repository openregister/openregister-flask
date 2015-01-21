from thingstance import Thing
from thingstance.stores.mongodb import MongoStore

database = "thingstance"

repositories = {}


class Repository(Thing):
    def __init__(self, name, *args, **kwargs):
        self.store = MongoStore(database=database, collection=name)
        repositories[name] = self
        Thing.__init__(self, name=name, *args, **kwargs)

Repository(name='thingstance', tagsHeld={'Register'})
Repository(name='education', tagsHeld={'Register'})
Repository(name='school', tagsHeld={'School', 'Headteacher'})
