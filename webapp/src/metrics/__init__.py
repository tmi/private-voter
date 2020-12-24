import prometheus_client
from flask import Response
# from prometheus_client import Counter

httpEndpointCounter = prometheus_client.Counter("privateVoter_httpEndpointCounter", "Counter for http endpoints", ['method', 'endpoint'])

def initMetrics(application):
    @application.route('/metrics')
    def metrics():
        return Response(prometheus_client.generate_latest(), mimetype=prometheus_client.CONTENT_TYPE_LATEST)
