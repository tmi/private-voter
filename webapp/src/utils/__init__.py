import metrics
import logging
import flask
import collections
from typing import Dict, Any, NamedTuple, Type, Callable, TypeVar

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
    def hasValOfType(content: Dict[str, Any], valName: str, valType: Type[T], extraCheck: Callable[[T], bool]) -> bool:
        return (valName in content) and (type(content[valName]) == valType) and extraCheck(content[valName])
    assertPredicateReport(hasValOfType(jsonContent, "options", str, lambda s : len(s) > 0), "createPollOptionsMissing", "/create poll call missing 'options' string param")
    options = jsonContent["options"]
    if (hasValOfType(jsonContent, "extraVotes", int, lambda d: d >= 0)):
        extraVotesMin = jsonContent["extraVotes"]
        extraVotesMax = jsonContent["extraVotes"]
    elif (hasValOfType(jsonContent, "extraVotesMin", int, lambda d: d >= 0) and hasValOfType(jsonContent, "extraVotesMax", int, lambda d: d >= 0)):
        extraVotesMin = jsonContent["extraVotesMin"]
        extraVotesMax = jsonContent["extraVotesMax"]
        assertPredicateReport(extraVotesMin <= extraVotesMax, "createPollExtraVotesMissing", "/create poll call missing correct 'extra votes' specification")
    else:
        assertPredicateReport(False, "createPollExtraVotesMissing", "/create poll call missing correct 'extra votes' specification")
    return PollParams(pollName, extraVotesMin, extraVotesMax, options)

