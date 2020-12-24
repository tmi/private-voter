from flask import Flask
import logging
import config

application = Flask(__name__)

@application.route('/status', methods = ['GET'])
def statusCall():
    logging.info("/status call received")
    return "long live and prosper"

def main():
    logging.debug("application starting")

    logging.debug("initialising default config")
    config.initDefault()
    logging.debug("initialising logging config")
    config.initLogging()

    logging.debug("application ready")

main()
