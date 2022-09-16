python ./services/01-app-uninstrumented.py &
python ./services/02-app-instrumented.py &
python ./services/03-app-instrumented-handled-errors.py &
python ./services/04-app-instrumented-custom-span.py &
python ./services/05-app-instrumented-custom-context.py &
python ./services/06-app-ecs-logging.py &
python ./services/07-app-ecs-logging-distributed.py &
python ./services/08-app-ecs-logging-distributed.py &
python ./services/11-app-otel.py &

#!/bin/bash
trap 'pkill -P $$' SIGINT SIGTERM INT

while true; 
do 
  curl localhost:5001/endpoint1;  
  curl localhost:5002/endpoint1;  
  curl localhost:5003/endpoint1;  
  curl localhost:5004/endpoint1;  
  curl localhost:5005/endpoint1;  
  curl localhost:5006/endpoint1;  
  curl localhost:5007/endpoint1;   
  sleep 0.5;
done &
wait
