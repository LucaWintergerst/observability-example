from flask import Flask

# instrument flask with Elastic APM
from elasticapm.contrib.flask import ElasticAPM
import elasticapm
import random
import time

import logging
import redis

# disable the default flask logger
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Log to a file
handler = logging.FileHandler(filename='/tmp/service2.log')
logger.addHandler(handler)

app = Flask(__name__)

server_url = 'https://community-conference.apm.us-central1.gcp.cloud.es.io'
service_name = '02-app-instrumented'
environment = 'dev'

# this is just an example token - please replace with your token that you get from Elastic Cloud or your APM Server
token = 'if0SfRh1EhBu7UiBru'
apm = ElasticAPM(app, server_url=server_url, service_name=service_name, environment=environment,
                 secret_token=token)

r = redis.Redis(host='localhost', port=6379, db=0)

# redis, slow and fast requests
@app.route("/endpoint1")
def endpoint1():
    logger.info("Received request")

    logger.info('connecting to Redis 20 times')
    for x in range(20):
        r.get('key1')

    # slow down the request 10% of the time
    if random.randint(0,9) < 1:
        time.sleep(0.02)
        logger.info('slow request')
    else:
        logger.info('fast request')

    # we'll try to do something here that might fail
    try:
        # we fail for 10% of all requests
        if random.randint(0, 9) < 1:
            time.sleep(0.1)
            raise RuntimeError('Failed to do something')
    except Exception as e:
        logger.error(e)

    return "Redis and slow and fast"

app.run(host='0.0.0.0', port=5002)
