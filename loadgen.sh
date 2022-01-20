while true; 
do 
  curl localhost:5001/endpoint1; 
  curl localhost:5002/endpoint1; 
  curl localhost:5003/endpoint1; 
  curl localhost:5004/endpoint1; 
  sleep 1;
done
