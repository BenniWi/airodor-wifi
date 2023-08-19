#!/bin/bash

if lsof -Pi :3849 -sTCP:LISTEN -t
then
    echo "port 3849 already in use, probably the web app is already running" 
else
    echo "starting airodor web app on port 3849"
    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
    cd $SCRIPT_DIR
    git pull
    cd airodor_web_app
    poetry install
    cd airodor_web_app
    poetry run flask run --host=0.0.0.0 --port=3849 --debug=False
fi

