#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/..

source `conda info --base`/etc/profile.d/conda.sh
conda activate private-voter

# for reasons unknown, the setuptools is causing trouble
pip list --format=freeze | grep -v setuptools > requirements.txt

zip privateVoterFront.zip -r privateVoterFront

docker build -t private-voter -f docker/Dockerfile .

rm privateVoterFront.zip requirements.txt
