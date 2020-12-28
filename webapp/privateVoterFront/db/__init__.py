import sqlite3
from typing import List
from privateVoterFront.utils import PollParams, assertPredicateReport, PrivatisedVote, PublicVote, VoterReport, VotedReport

votedTable = """create table voted (
voted_randomId text primary key,
pollId text,
votedOption text
)"""
votedInsert = "insert into voted(voted_randomId, pollId, votedOption) values (?, ?, ?)"
votedReport = "select votedOption, count(1) from voted where pollId = ? group by votedOption"

# note -- voterId is null in case of generated votes
voterTable = """create table voter (
voter_randomId text primary key,
pollId text,
voterId text
)"""
voterInsert = "insert into voter(voter_randomId, pollId, voterId) values (?, ?, ?)"
voterReport = "select count(distinct voterId) as realVoters, sum(voterId is not null) as realVotes, count(1) as totalVotes from voter where pollId = ?" # noqa: 501

pollsTable = """create table polls (
pollId text primary key,
extraVotesMin integer,
extraVotesMax integer,
options text
)"""
pollsInsert = "insert into polls(pollId, extraVotesMin, extraVotesMax, options) values (?, ?, ?, ?)"
pollsFetch = "select * from polls where pollId = ?"

# for readiness probe
testTable = """create table test (
rowId integer primary key,
value integer
)"""
readinessStatement = """insert into test(rowId, value) values (0, 0) on conflict(rowId) do update set value=value+1"""
versionStatement = """select sqlite_version();"""

# TODO this whole module needs a refact
# TODO we are using a single connection due to how in mem sqlite3 works
connection = None
def getConnection():
    if not connection:
        raise NotImplementedError("too early db call")
    return connection
def shutdown():
    if connection:
        connection.close()

def initLocalDb() -> None:
    global connection
    # we presume sqlite to be thread-safe compiled as that is the default
    connection = sqlite3.connect(':memory:', check_same_thread = False)

    # possibly to be done in the main method, if made robust
    connection.execute(testTable)
    connection.execute(voterTable)
    connection.execute(votedTable)
    connection.execute(pollsTable)
    connection.commit()

def initDb(mode: str) -> None:
    if (mode == 'local'):
        initLocalDb()

def readinessCall() -> bool:
    try:
        getConnection().execute(readinessStatement)
    except sqlite3.OperationalError as e:
        vs = getConnection().execute(versionStatement).fetchone()
        import platform
        vp = platform.python_version()
        raise Exception(f"received operational error {e} ({e.args[0]}), with sqlite version being {vs} and python version being {vp}") # noqa: 501
    return True

def persistCreatePoll(pollParams: PollParams) -> None:
    try:
        c = getConnection()
        c.execute(pollsInsert, (pollParams.pollId, pollParams.extraVotesMin, pollParams.extraVotesMax, pollParams.options))
        c.commit()
    except sqlite3.IntegrityError: # TODO this will be a problem when introducing more dbs
        assertPredicateReport(
            False,
            "createPollDuplicateId",
            "/create poll not possible because a poll of such name already exists"
        )

def getPollParams(pollName) -> PollParams:
    c = getConnection()
    result = c.execute(pollsFetch, (pollName,)).fetchone()
    if not result:
        assertPredicateReport(False, "votePollNotExists", "/vote attempted for a non-existent poll, what a trickery!")
    else:
        return PollParams(result[0], result[1], result[2], result[3])

def persistVoting(voted: List[PrivatisedVote], voters: List[PublicVote]) -> None:
    c = getConnection()
    c.executemany(voterInsert, ((e.randomId_voter, e.pollId, e.voterId) for e in voters))
    c.executemany(votedInsert, ((e.randomId_voted, e.pollId, e.votedOption) for e in voted))
    c.commit()

def getVoterReport(pollName: str) -> VoterReport:
    c = getConnection()
    # TODO check if poll exists
    realVoters, realVotes, totalVotes = c.execute(voterReport, (pollName,)).fetchone()
    return VoterReport(realVoters, realVotes if realVotes is not None else 0, totalVotes)

def getVotedReport(pollName: str) -> List[VotedReport]:
    c = getConnection()
    # TODO check if poll exists
    return [VotedReport(optionName, optionVotes) for optionName, optionVotes in c.execute(votedReport, (pollName,)).fetchall()]
