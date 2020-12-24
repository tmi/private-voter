import metrics
import logging
import flask

class InputError(Exception):
    def __init__(self, message):
        self.message = message

def assertPredicateReport(predicate, errorType, errorMessage):
    if not predicate:
        metrics.errorCounter.labels(errorType = errorType).inc()
        logging.debug(errorMessage)
        raise InputError(errorMessage + '\n')
