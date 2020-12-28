import logging
import random
from typing import Dict, Any, NamedTuple, Type, Callable, TypeVar, Tuple, List
import uuid
import privateVoterFront.config as config
import privateVoterFront.metrics as metrics

class PollParams(NamedTuple):
    pollId: str
    extraVotesMin: int
    extraVotesMax: int
    options: str

class InputError(Exception):
    def __init__(self, message):
        self.message = message

def assertPredicateReport(predicate: bool, errorType: str, errorMessage: str) -> None:
    if not predicate:
        metrics.errorCounter.labels(errorType = errorType).inc()
        logging.debug(errorMessage)
        raise InputError(errorMessage + '\n')

def parsePollParams(jsonContent: Dict[str, Any], pollName: str) -> PollParams:
    pollName = pollName
    T = TypeVar('T')
    maxOptionsLength = int(config.get("DB", "MAXOPTLEN"))

    def hasValOfType(content: Dict[str, Any], valName: str, valType: Type[T], extraCheck: Callable[[T], bool]) -> bool:
        return (valName in content) and (type(content[valName]) == valType) and extraCheck(content[valName])

    assertPredicateReport(
        hasValOfType(jsonContent, "options", str, lambda s: len(s) > 0 and len(s) < maxOptionsLength),
        "createPollOptionsMissing",
        "/create poll call missing valid 'options' string param"
    )
    options = jsonContent["options"]
    if (hasValOfType(jsonContent, "extraVotes", int, lambda d: d >= 0)):
        extraVotesMin = jsonContent["extraVotes"]
        extraVotesMax = jsonContent["extraVotes"]
    elif (hasValOfType(jsonContent, "extraVotesMin", int, lambda d: d >= 0) and
            hasValOfType(jsonContent, "extraVotesMax", int, lambda d: d >= 0)):
        extraVotesMin = jsonContent["extraVotesMin"]
        extraVotesMax = jsonContent["extraVotesMax"]
        assertPredicateReport(
            extraVotesMin <= extraVotesMax,
            "createPollExtraVotesMissing",
            "/create poll call missing correct 'extra votes' specification"
        )
    else:
        assertPredicateReport(
            False,
            "createPollExtraVotesMissing",
            "/create poll call missing correct 'extra votes' specification"
        )
    return PollParams(pollName, extraVotesMin, extraVotesMax, options)

class PrivatisedVote(NamedTuple):
    randomId_voted: str
    pollId: str
    votedOption: str

class PublicVote(NamedTuple):
    randomId_voter: str
    pollId: str
    voterId: str

# so this fction
# 1. takes a single received vote,
# 2. augments it with randomly generated votes,
# 3. splits into a "public" voter part and "private" voted part and shuffles each independently
# 4. the return values are to be persisted in respective tables
def privateVotingBusinessLogic(votedOption: str, voterId: str, pollParams: PollParams) -> Tuple[List[PrivatisedVote], List[PublicVote]]: # noqa: E501
    logging.debug("shuffling and enriching the received vote")
    extraVotes = random.randint(pollParams.extraVotesMin, pollParams.extraVotesMax)
    allOptions = list(set(pollParams.options.split(":")))
    assertPredicateReport(
        votedOption in allOptions,
        "voteOptionNotAllowed",
        "/vote for option that wasnt specified during /create"
    )
    votedOptions = random.choices(allOptions, k = extraVotes) + [votedOption]
    voterIds = [None for i in range(extraVotes)] + [voterId]
    privateParts = [PrivatisedVote(str(uuid.uuid4()), pollParams.pollId, votedOption) for votedOption in votedOptions]
    publicParts = [PublicVote(str(uuid.uuid4()), pollParams.pollId, voterId) for voterId in voterIds]
    random.shuffle(privateParts)
    random.shuffle(publicParts)
    return (privateParts, publicParts)

class VoterReport(NamedTuple):
    realVoters: int
    realVotes: int
    totalVotes: int

class VotedReport(NamedTuple):
    optionName: str
    optionVotes: int

# possibly replace Any with recusive type
def combineReports(votedReport: VoterReport, voterReport: VotedReport) -> Dict[str, Any]:
    # this is really ugly
    d = {}
    d['totalVotes'] = voterReport.totalVotes
    d['realVotes'] = voterReport.realVotes
    d['generatedVotes'] = voterReport.totalVotes - voterReport.realVotes
    d['realVoters'] = voterReport.realVoters
    d['duplicatedVotes'] = voterReport.realVotes - voterReport.realVoters
    o = [{"optionName": optionName, "optionVotes": optionVotes} for optionName, optionVotes in votedReport]
    return {'voterStats': d, 'optionStats': o}
