from flask import Flask
import logging

application = Flask(__name__)

@application.route('/status', methods = ['GET'])
def statusCall():
    logging.info("/status call received")
    return "long live and prosper"

def main():
    logging.debug("application starting")

main()
