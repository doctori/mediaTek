#VARIABLES
DBIMAGE=mediatek_db:latest
WEBIMAGE=mediatek_web:latest


#first erase old docker instances
echo "Going to clean the workspace"
docker rm -f $(docker ps  -a --filter 'exited=0' | grep ${DBIMAGE} | awk '{print $1}')

docker rm -f $(docker ps  -a --filter 'exited=0' | grep ${WEBIMAGE} | awk '{print $1}')
echo "rebuilding"
docker-compose build
echo "Starting our env "
docker-compose up -d

docker exec -i -t mediatek_web_1 bash

