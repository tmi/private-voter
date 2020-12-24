#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/..

source `conda info --base`/etc/profile.d/conda.sh
conda activate private-voter
pip freeze > webapp_requirements.txt

docker build -t private-voter -f docker/Dockerfile .
