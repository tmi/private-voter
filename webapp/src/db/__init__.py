import sqlite3

# TODO
votesTable = """create table voted (
pollId text,
randomVoterId text,
votedId text)"""

# TODO
voterTable = """create table voter (
pollId text,
voterId text,
isGenerated integer
)"""

# for readiness probe
testTable = """create table test (
rowId integer primary key,
value integer
)"""

readinessStatement = """insert into test(rowId, value) values (0, 0) on conflict(rowId) do update set value=value+1"""

class DbWrapper():
    @staticmethod
    def getConnection():
        raise NotImplementedError("too early db call") # to be overriden later

    @staticmethod
    def shutdown():
        raise NotImplementedError("too early db call") # to be overriden later

def initLocalDb():
    DbWrapper.connection = sqlite3.connect(':memory:', check_same_thread = False) # we presume sqlite to be thread-safe compiled as that is the default
    def getLocalConnection():
        return DbWrapper.connection
    def localShutdown():
        DbWrapper.connection.close()
    DbWrapper.getConnection = getLocalConnection
    DbWrapper.shutdown = localShutdown

    connection = DbWrapper.getConnection() # possibly to be done in the main method, if made robust
    connection.execute(testTable)
    connection.commit()

def initDb(mode):
    if (mode == 'local'):
        return initLocalDb()

def readinessCall():
    DbWrapper.getConnection().execute(readinessStatement)
    return True
