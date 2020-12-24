#!/bin/bash
set -x
DEFAULT_URL="localhost"
export URL=${1:-$DEFAULT_URL}
DEFAULT_PORT="80"
export PORT=${2:-$DEFAULT_PORT}

export POLL_ID="testpoll"
export VOTER_ID="testvoter"
export VOTED_ID="option1"

export POLLDEF="{\"options\": [ {\"optionName\": \"option1\"}, {\"optionName\": \"option2\"} ] }"

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
        curl -k -XPOST ${URL}:${PORT}/vote/${POLL_ID}?voterId=${VOTER_ID}\&votedId=${VOTED_ID}
}

status
readiness
createPoll
votePoll

export POLL_ID=""
createPoll
votePoll

export POLL_ID="testpoll"
export POLLDEF=""
createPoll

export VOTER_ID=""
votePoll
