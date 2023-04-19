#!/bin/bash

if lsof -Pi :5000 -sTCP:LISTEN -t
then
    echo "port 5000 already in use, probably the web app is already running" 
else
    echo "starting airodor web app on port 5000"
    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
    cd $SCRIPT_DIR
    git pull
    cd airodor_web_app
    poetry install
    cd airodor_web_app
    poetry run flask run --host=0.0.0.0
fi

