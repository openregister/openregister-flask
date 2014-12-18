#!/bin/bash

. ../environment.sh

echo 'db.things.remove("")' | mongo
../manage.py load_data -s ../data/data/
