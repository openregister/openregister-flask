#!/bin/bash

. ../environment.sh

echo 'db.entries.remove("")' | mongo
../manage.py load_data -s ../data/data/
