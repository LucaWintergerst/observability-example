from flask import Flask
import os
from dotenv import load_dotenv

# instrument flask with Elastic APM
from elasticapm.contrib.flask import ElasticAPM
import elasticapm
import random
import time
import structlog

import ecs_logging
import logging
import redis

load_dotenv()

# disable the default flask logger
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Log to a file
handler = logging.FileHandler(filename='/tmp/service6.log')
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)

from elasticapm.handlers.structlog import structlog_processor
structlog.configure(
    processors=[structlog_processor,ecs_logging.StructlogFormatter()],
    wrapper_class=structlog.BoundLogger,
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory()
)



app = Flask(__name__)

app.config['ELASTIC_APM'] = {
    'SERVER_URL': os.environ["SERVER_URL"],
    'SERVICE_NAME': '06-app-ecs-logging',
    'SECRET_TOKEN': os.environ["SECRET_TOKEN"],
    'ENVIRONMENT':  'dev'
}
apm = ElasticAPM(app)

apm_client = elasticapm.get_client()

r = redis.Redis(host='localhost', port=6379, db=0)
r.ping()

@app.before_request
def do_something_whenever_a_request_comes_in():
    elasticapm.set_user_context(
        username="john", 
        email="someone@example.com", 
        user_id="123-123-123"
    )

# redis, slow and fast requests
@app.route("/endpoint1")
def endpoint1():
    logger.info("Received request", extra={"http.request.method": "get"})

    logger.info('connecting to Redis 20 times')
    for x in range(20):
        r.get('key1')

    # slow down the request 10% of the time
    if random.randint(0,9) < 1:
        with elasticapm.capture_span('this is a slow span'):
            elasticapm.set_custom_context({'slow_request_stats': 1})
            elasticapm.label(label1='slowed down deliberately')
            time.sleep(0.02)
            logger.info('slow request')
    else:
        with elasticapm.capture_span('this is a fast span'):
            logger.info('fast request')

    # we'll try to do something here that might fail
    try:
        # we fail for 10% of all requests
        if random.randint(0, 9) < 1:
            time.sleep(0.1)
            raise RuntimeError('expected error, will be handled')
    except Exception as e:
        logger.error(e)
        apm_client.capture_exception(handled=True)
        elasticapm.set_transaction_outcome(outcome='failure')
        return "endpoint1, error"

    if random.randint(0, 9) < 1:
        time.sleep(0.1)
        raise RuntimeError('unexpected error')

    return "endpoint1"

app.run(host='0.0.0.0', port=5006)
