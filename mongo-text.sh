#!/bin/sh
set -ex

until nc -z localhost 27017; do
  echo "Waiting for MongoDB"
  sleep 1
done

mongo admin --eval 'db.adminCommand({setParameter: true, textSearchEnabled: true})'
