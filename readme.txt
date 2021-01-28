# build docker image
docker build -t panties .

# run
docker run -p 80:8080 --rm panties

# run with volume mounted
docker run -p 80:8080 -v ${PWD}:/app --rm panties


#.env variables

URL1='https://dx-api-ru1.thingpark.com/core/latest/api/baseStations?healthState=ACTIVE&connectionState=CNX&statistics=true&commercialDetails=true'
URL2='http://172.17.0.1:8083/api/monitoring/gateways/actility_styled'

AUTH1='Bearer '
AUTH2=''

REQUEST_TIME = 180