#!/bin/bash
# set -x
DEFAULT_URL="localhost"
export URL=${1:-$DEFAULT_URL}
DEFAULT_PORT="80"
export PORT=${2:-$DEFAULT_PORT}

export POLL_ID="testpoll1"
export VOTER_ID="testvoter"
export VOTED_ID="option1"

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
        curl -k -XPOST ${URL}:${PORT}/vote/${POLL_ID}?voterId=${VOTER_ID}\&votedId=${VOTED_ID}
}

echo "Rudimentary checks, all should pass"
status
readiness
createPoll
votePoll

echo "Missing poll id, all should fail"
export POLL_ID=""
createPoll
votePoll

echo "Duplicate poll id, should fail"
export POLL_ID="testpoll1"
createPoll

echo "Missing poll content, should fail"
export POLL_ID="testpoll2"
export POLLDEF=""
createPoll

echo "Wrong extra votes specs, all should fail"
export POLL_ID="testpollW1"
export POLLDEF="{\"options\": \"opt1:opt2\", \"extraVotes\": -1 }"
createPoll
export POLLDEF="{\"options\": \"opt1:opt2\", \"extraVotesMin\": 3, \"extraVotesMax\": 2 }"
createPoll

echo "Missing voter id, should fail"
export VOTER_ID=""
votePoll
