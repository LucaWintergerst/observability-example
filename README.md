### Overview

This repo contains a small python service using flask. The service is available in 4 stages. 

1 - without any instrumentation

2 - with basic Elastic APM instrumentation

3 - with a more advanced Elastic APM instrumentation

4 - with full instrumentation and ECS logging

### Requirements
Redis is required for the services to run.

```
docker run -p 6379:6379 -d redis
```


A Python venv is recommended:
```
virtualenv -p python3 .venv
source .venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Before running the services, make sure you provide the following endpoints and credentials:
```
APM:
server_url
token

Filebeat: 
cloud.id: deploymentname:secret123
cloud.auth: elastic:secret123
or 
output.elasticsearch:
  hosts: ["localhost:9200"]
  username: "elastic"
  password: "changeme"
```

You can download Filebeat here: https://www.elastic.co/downloads/beats/filebeat

APM-Server, Elasticsearch and Kibana also need to be running. You can find more information about the Elastic Stack [here](https://www.elastic.co/elastic-stack/)

### Running the Python Services
To run the python services, execute the following command for the file you'd like to run:
```
python 01-app-uninstrumented.py
python 02-app-instrumented.py
python 03-app-instrumented-compression.py
python 04-app-ecs-logging.py
```

### Running the Loadgenerator
The loadgenerator is just a simple bash script that runs a curl request against each service in a loop. 

```
sh loadgen.sh
```


### Screenshots of Kibana

![screencapture-community-conference-kb-us-central1-gcp-cloud-es-io-9243-app-apm-services-04-app-ecs-logging-overview-2022-01-20-10_43_46](https://user-images.githubusercontent.com/11661400/150313736-05bf3ddf-1b82-40e8-94d0-948f04a75ecb.png)
![screencapture-community-conference-kb-us-central1-gcp-cloud-es-io-9243-app-apm-services-04-app-ecs-logging-transactions-view-2022-01-20-10_44_23](https://user-images.githubusercontent.com/11661400/150313846-bff9ae02-4d6c-4ef9-844e-ff1aa265a727.png)
