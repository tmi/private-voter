from flask import Flask
import logging
import config
import metrics

application = Flask(__name__)

@application.route('/status', methods = ['GET'])
def statusCall():
    logging.info("/status call received")
    metrics.httpEndpointCounter.labels(method = 'get', endpoint = '/status').inc()
    return "long live and prosper"

def main():
    logging.debug("application starting")

    logging.debug("initialising default config")
    config.initDefault()
    logging.debug("initialising logging config")
    config.initLogging()
    logging.debug("initialising metrics")
    metrics.initMetrics(application)

    logging.debug("application ready")

main()
