import flask
import logging
import config
import metrics

initFinalised = False
application = flask.Flask(__name__)

@application.route('/status', methods = ['GET'])
def statusCall(): # to be used as a liveness probe
    logging.info("/status call received")
    metrics.httpEndpointCounter.labels(method = 'get', endpoint = '/status').inc()
    return "long live and prosper"

@application.route('/readiness', methods = ['GET'])
def readinessCall():
    # TODO create a decorator that would automatically add the logging and metrics calls
    logging.info("/readiness call received")
    metrics.httpEndpointCounter.labels(method = 'get', endpoint = '/readiness').inc()

    global initFinalised
    # once we have DB and Queue clients, we will check their instantiation here
    if (initFinalised):
        return flask.Response("all ready", status = 200, mimetype = 'text/plain')
    else:
        return flask.Response("init not finalised", status = 400, mimetype = 'text/plain')


def main():
    logging.debug("application starting")

    logging.debug("initialising default config")
    config.initDefault()
    logging.debug("initialising logging config")
    config.initLogging()
    logging.debug("initialising metrics")
    metrics.initMetrics(application)

    logging.debug("application ready")
    global initFinalised
    initFinalised = True

main()
