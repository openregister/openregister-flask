import os
import logging
import csv

from io import (
    BytesIO,
    TextIOWrapper
)

from zipfile import ZipFile
from urllib.request import urlopen

from entry import Entry
from entry.stores.mongodb import MongoStore
from application.utils import log_traceback

registers = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())


class Register(Entry):
    def __init__(self, name, mongo_uri, *args, **kwargs):
        collection = name.lower()
        self.store = MongoStore(mongo_uri, collection=collection)
        registers[collection] = self
        Entry.__init__(self, name=name, *args, **kwargs)

    def put(self, entry):
        self.store.put(entry)

    def find(self, query, page):
        return self.store.find(query, page)

    def size(self):
        return self.store.entries.count()

    # TBD: move to entry store / representations
    def load(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:

                path = os.path.join(root, file)
                suffix = os.path.splitext(path)[1]

                # this belong in representation / entry

                # file of many entries ..
                if suffix == ".tsv":
                    import csv
                    with open(path) as f:
                        reader = csv.DictReader(f, delimiter='\t')
                        for d in reader:
                            if len(d.keys()):
                                entry = Entry()
                                entry.primitive = d
                                self.store.put(entry)

                else:
                    # assumes one entry per-file.
                    print("slurping %s" % path)
                    text = open(path).read()

                    entry = Entry()
                    if suffix == ".yaml":
                        entry.yaml = text
                    elif suffix == ".json":
                        entry.json = text

                    self.put(entry)

    def load_remote(self, url):
        try:
            result = urlopen(url).read()
            print('Done reading')
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
                        entry = Entry()
                        entry.yaml = file_contents.read()
                        self.put(entry)
                    elif name.endswith('.tsv'):
                        reader = csv.DictReader(file_contents, delimiter='\t')
                        for row in reader:
                            if len(row.keys()):
                                entry = Entry()
                                entry.primitive = row
                                self.store.put(entry)

                    print('stored', name)

        except Exception as ex:
            log_traceback(logger, ex)

