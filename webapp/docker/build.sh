#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/..

source `conda info --base`/etc/profile.d/conda.sh
conda activate private-voter

# TODO fail if bad
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --ignore=E302,E251,E226,E261,W504

# TODO fail if bad
pytest .

# for reasons unknown, the setuptools is causing trouble; and we dont need pytest and flake
pip list --format=freeze | grep -v setuptools | grep -v pytest | grep -v flake > requirements.txt

zip privateVoterFront.zip -r privateVoterFront

docker build -t private-voter -f docker/Dockerfile .

rm privateVoterFront.zip
