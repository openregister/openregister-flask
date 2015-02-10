import os
import logging

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

from thingstance import Thing
from thingstance.stores.mongodb import MongoStore
from application.utils import log_traceback

registers = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


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


    def load_remote(self, url):
        lines = []
        try:
            result = urlopen(url).read()
            stream = BytesIO(result)
            zipfile = ZipFile(stream, 'r')
            #TODO - handle json and other formats
            file_names = [name for name in zipfile.namelist() if name.endswith('yaml')]

            for name in file_names:
                l = [line.decode('utf-8') for line in zipfile.open(name).readlines()]
                data = ''.join(l)
                lines.append(data)
                thing = Thing()
                thing.yaml = data
                self._store.put(thing)
        except Exception as ex:
            log_traceback(logger, ex)

        return lines

