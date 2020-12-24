import flask
import logging
import config
import metrics
import utils
import json
import db

initFinalised = False
application = flask.Flask(__name__)

@application.route('/status', methods = ['GET'])
def statusCall(): # to be used as a liveness probe
    try:
        logging.info("/status call received")
        metrics.httpEndpointCounter.labels(method = 'get', endpoint = '/status').inc()
        return "long live and prosper\n"
    except Exception as e:
        return flask.Response(f"/status call failed due to {e}", status = 400, mimetype = 'text/plain')

@application.route('/readiness', methods = ['GET'])
def readinessCall():
    try:
        # TODO create a decorator that would automatically add the logging and metrics calls
        logging.info("/readiness call received")
        metrics.httpEndpointCounter.labels(method = 'get', endpoint = '/readiness').inc()

        global initFinalised
        if (not initFinalised):
            return flask.Response("init not finalised\n", status = 400, mimetype = 'text/plain')
        if (not db.readinessCall()):
            return flask.Response("database not ready\n", status = 400, mimetype = 'text/plain') # probably extraneous as unready database raises
        return flask.Response("all ready\n", status = 200, mimetype = 'text/plain')
    except Exception as e:
        return flask.Response(f"/readiness call failed due to {e}", status = 400, mimetype = 'text/plain')


@application.route('/create/<pollName>', methods = ['POST'])
def createPoll(pollName):
    try:
        # TODO create a decorator to automate the try-catch
        logging.info(f"/create call received for poll {pollName}")
        metrics.httpEndpointCounter.labels(method = 'vote', endpoint = '/create').inc()

        utils.assertPredicateReport(bool(pollName), "createPollNameNotPresent", "/create call missing <pollName> path param")

        utils.assertPredicateReport(flask.request.content_type == 'application/json' and flask.request.is_json, "createPollContentNotPresent", "/create call missing the json body")
        try:
            content = json.loads(flask.request.get_data())
        except json.decoder.JSONDecodeError as e:
            utils.assertPredicateReport(False, "createPollContentNotValid", "/create call not having valid json body")
        utils.assertPredicateReport(bool(content), "createPollContentNotPresent", "/create call missing the json body")
        # TODO impl
        return f"ok: poll {pollName} created with params {content}\n"
    except utils.InputError as e:
        return flask.Response(e.message, status = 400, mimetype='text/plain')
    except Exception as e:
        logging.error(f"encountered {e}")
        return flask.Response(f"error handling stuff because of {e}\n", status = 400, mimetype='text/plain')

@application.route('/vote/<pollName>', methods = ['POST'])
def vote(pollName):
    try:
        logging.info(f"/vote call received for poll {pollName}")
        metrics.httpEndpointCounter.labels(method = 'post', endpoint = '/vote').inc()

        utils.assertPredicateReport(bool(pollName), "votePollNameNotPresent", "/vote call missing <pollName> path param")
        voterId = flask.request.args.get('voterId')
        votedId = flask.request.args.get('votedId')
        utils.assertPredicateReport(bool(voterId), "voteVoterIdNotPresent", "/vote call missing <voterId> request param")
        utils.assertPredicateReport(bool(votedId), "voteVotedIdNotPresent", "/vote call missing <votedId> request param")

        # TODO impl
        return f"ok: in poll {pollName} the voter {voterId} voted for {votedId}\n"
    except utils.InputError as e:
        return flask.Response(e.message, status = 400, mimetype='text/plain')
    except Exception as e:
        logging.error(f"encountered {e}")
        return flask.Response(f"error handling stuff because of {e}\n", status = 400, mimetype='text/plain')

def main():
    logging.debug("application starting")

    logging.debug("initialising default config")
    config.initDefault()
    logging.debug("initialising logging config")
    config.initLogging()
    logging.debug("initialising metrics")
    metrics.initMetrics(application)
    logging.debug("initialising database")
    db.initDb("local") # TODO config

    logging.debug("application ready")
    global initFinalised
    initFinalised = True

main()
