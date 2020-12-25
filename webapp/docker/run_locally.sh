#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR
docker run -p 80:80 -it --rm --env INI_FILE="/webapp/config.ini" -v "$(pwd)/local_run.ini":"/webapp/config.ini" private-voter
