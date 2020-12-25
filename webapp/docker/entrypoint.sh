#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR

# export FLASK_APP="src/app.py"
export FLASK_APP="privateVoterFront.zip/privateVoterFront"
echo "iniFile: $INI_FILE"

python -m flask run --host='0.0.0.0' --port=80
