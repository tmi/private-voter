import sqlite3
from utils import PollParams, assertPredicateReport
from typing import Any
import logging

votedTable = """create table voted (
voted_randomId text primary key,
pollId text,
votedId text
)"""

voterTable = """create table voter (
voter_randomId text primary key,
pollId text,
voterId text,
isGenerated integer
)"""

pollsTable = """create table polls (
pollId text primary key,
extraVotesMin integer,
extraVotesMax integer,
options text
)"""
pollsInsert = "insert into polls(pollId, extraVotesMin, extraVotesMax, options) values (?, ?, ?, ?)"

# for readiness probe
testTable = """create table test (
rowId integer primary key,
value integer
)"""
readinessStatement = """insert into test(rowId, value) values (0, 0) on conflict(rowId) do update set value=value+1"""

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
    connection = sqlite3.connect(':memory:', check_same_thread = False) # we presume sqlite to be thread-safe compiled as that is the default

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
    getConnection().execute(readinessStatement)
    return True

def persistCreatePoll(pollParams: PollParams) -> None:
    try:
        c = getConnection()
        c.execute(pollsInsert, (pollParams.pollId, pollParams.extraVotesMin, pollParams.extraVotesMax, pollParams.options))
        c.commit()
    except sqlite3.IntegrityError as e: # TODO this will be a problem when introducing more dbs
        assertPredicateReport(False, "createPollDuplicateId", "/create poll not possible because a poll of such name already exists")
