import pytest
import json

import privateVoterFront

@pytest.fixture
def client():
    privateVoterFront.application.config["TESTING"] = True

    with privateVoterFront.application.test_client() as client:
        yield client

def test_status(client):
    rv = client.get('/status')
    assert rv.status_code == 200

def test_readiness(client):
    rv = client.get('/readiness')
    assert rv.status_code == 200

def test_createOk(client):
    pollId = "poll1"
    rv = client.post(f'/create/{pollId}', json = dict(options="opt1:opt2", extraVotes=3))
    assert rv.status_code == 200

def test_createNoJson(client):
    pollId = "poll2"
    rv = client.post(f'/create/{pollId}', json = dict())
    assert rv.status_code == 400

def test_createVote(client):
    rvs = []
    pollId = "poll3"
    rvs += [client.post(f'/create/{pollId}', json = dict(options="opt1:opt2", extraVotes=3)).status_code]
    voter1 = "voter1"
    rvs += [client.post(f"/vote/{pollId}?voterId={voter1}&votedOption=opt1").status_code]
    assert set(rvs) == set([200])

def test_voteMissingArgs(client):
    pollId = "poll4"
    voter1 = "voter1"
    rv0 = client.post(f'/create/{pollId}', json = dict(options="opt1:opt2", extraVotes=3))
    rv1 = client.post(f"/vote/{pollId}?voterId={voter1}")
    rv2 = client.post(f"/vote/{pollId}?votedOption=opt1")
    assert rv1.status_code == 400 and rv2.status_code == 400 and rv0.status_code == 200

def test_voteNonExistent(client):
    voter1 = "voter1"
    nonExistentPollId = "pollX"
    rv = client.post(f"/vote/{nonExistentPollId}?voterId={voter1}&votedOption=opt1")
    assert rv.status_code == 400

def test_report(client):
    voter1 = "voter1"
    voter2 = "voter2"
    pollId = "pollR"
    rvs = []
    rvs += [client.post(f'/create/{pollId}', json = dict(options="opt1:opt2", extraVotes=3)).status_code]
    rvs += [client.post(f"/vote/{pollId}?voterId={voter1}&votedOption=opt1").status_code]
    rvs += [client.post(f"/vote/{pollId}?voterId={voter1}&votedOption=opt1").status_code]
    rvs += [client.post(f"/vote/{pollId}?voterId={voter2}&votedOption=opt2").status_code]
    report = client.get(f"/report/{pollId}")
    rvs += [report.status_code]
    assert set(rvs) == set([200])
    jd = report.get_json()
    vs = jd['voterStats']
    assert vs['totalVotes'] == 3*(3+1)
    assert vs['realVotes'] == 3
    assert vs['generatedVotes'] == 3*3
    assert vs['realVoters'] == 2
    assert vs['duplicatedVotes'] == 1
    os = jd['optionStats']
    assert len(os) == 2
    assert set([o['optionName'] for o in os]) == set(['opt1', 'opt2'])
    assert sum([o['optionVotes'] for o in os]) == 3*(3+1)
