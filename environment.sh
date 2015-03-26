#!/bin/sh
export MODE='dev'
export SETTINGS='config.Config'
export REGISTER_DOMAIN='openregister.dev'
export BASE_URL='http://'$REGISTER_DOMAIN
export MONGO_URI='mongodb://127.0.0.1:27017/thingstance'
export PAGE_SIZE='50'
export PORT='8000'
export SECRET_KEY='not-secret'
export HEROKU_KEY='not-secret'
export GITHUB_ORG='https://github.com/openregister'
