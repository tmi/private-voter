#!/bin/bash
# set -x
DEFAULT_URL="localhost"
export URL=${1:-$DEFAULT_URL}
DEFAULT_PORT="80"
export PORT=${2:-$DEFAULT_PORT}

export POLL_ID="testpoll1"
export VOTER_ID="testvoter"
export VOTED_OPTION="opt1"

export POLLDEF="{\"options\": \"opt1:opt2\", \"extraVotes\": 2 }"

function status() {
        curl -k -XGET ${URL}:${PORT}/status
}

function readiness() {
        curl -k -XGET ${URL}:${PORT}/readiness
}

function createPoll() {
        curl -k -XPOST -H 'Content-Type: application/json' ${URL}:${PORT}/create/${POLL_ID} -d "${POLLDEF}"
}

function votePoll() {
        curl -k -XPOST ${URL}:${PORT}/vote/${1}?voterId=${2}\&votedOption=${3}
}

function report() {
	curl -s -k -XGET ${URL}:${PORT}/report/${POLL_ID} | python -m json.tool
}
