import os
import logging
import csv

from io import (
    BytesIO,
    TextIOWrapper
)

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
                if suffix == ".tsv":
                    import csv
                    with open(path) as f:
                        reader = csv.DictReader(f, delimiter='\t')
                        for d in reader:
                            if len(d.keys()):
                                thing = Thing()
                                thing.primitive = d
                                self._store.put(thing)

                else:
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
        try:
            result = urlopen(url).read()
            stream = BytesIO(result)
            zipfile = ZipFile(stream, 'r')

            # TODO - handle json and other formats
            file_names = [name for name in zipfile.namelist()
                          if name.endswith('.yaml') or name.endswith('.tsv')]

            for name in file_names:
                with zipfile.open(name, 'r') as f:
                    file_contents = TextIOWrapper(f,
                                                  encoding='utf-8',
                                                  newline='')
                    if name.endswith('.yaml'):
                        thing = Thing()
                        thing.yaml = file_contents.read()
                        self._store.put(thing)
                    elif name.endswith('.tsv'):
                        reader = csv.DictReader(file_contents, delimiter='\t')
                        for row in reader:
                            if len(row.keys()):
                                thing = Thing()
                                thing.primitive = row
                                self._store.put(thing)

                    print('stored', name)

        except Exception as ex:
            log_traceback(logger, ex)
