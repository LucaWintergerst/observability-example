import logging
import ecs_logging

# Get the Logger
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Add an ECS formatter to the Handler
handler = logging.StreamHandler()
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)

# Emit a log!
for x in range(0, 10):
  logger.debug("Request received from 192.168.0.1", extra={"client.ip": "192.168.0.1"})
