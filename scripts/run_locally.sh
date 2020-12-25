#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $DIR/..

# this doesn't work, cf https://github.com/conda/conda/issues/7980
# conda init bash
# we instead do this:
source `conda info --base`/etc/profile.d/conda.sh

conda activate private-voter


export FLASK_APP="webapp/privateVoterFront"

python -m flask run --host='0.0.0.0' --port=80
