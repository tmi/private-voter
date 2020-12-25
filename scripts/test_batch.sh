#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/
source test_suite.sh
# set -x


echo "Rudimentary checks, all should pass"
status
readiness
createPoll
votePoll $POLL_ID $VOTER_ID $VOTED_OPTION

echo "Missing option / nonexistent poll id, both should fail"
votePoll $POLL_ID $VOTER_ID "badOption"
votePoll "badPollId" $VOTER_ID $VOTED_OPTION

echo "Missing poll id, all should fail"
export POLL_ID=""
createPoll
votePoll $POLL_ID $VOTER_ID $VOTED_OPTION

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
votePoll $POLL_ID $VOTER_ID $VOTED_OPTION

export POLL_ID="testpoll1"
report
