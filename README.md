# Api App for IoT Sensors
By using flask postgresql auth0 nginx uWsgi

## Requirements

* [Docker]
* [Docker-compose]


## Run

Clone the repo

    $ git clone git@github.com:maradwan/api-postgresql-auth0.git
    $ docker-compose up -d


## Create db data 

    $ docker exec -it db bash -c 'PGPASSWORD=password psql -h 127.0.0.1 -U postgres -d postgres -c "create database data;"'


## Create extension for uuid

    $ docker exec -it db bash -c PGPASSWORD=password psql -h 127.0.0.1 -U postgres -d data -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'

## Create random data in database

    $ docker exec -it db bash -c echo; for i in $(seq 25);  do  PGPASSWORD=password psql -h 127.0.0.1 -U postgres -d data -c "INSERT INTO raw_data (eventtime, devicename, item ,detailstatus,filename ,linenumber) VALUES ('`date "+%x %H:%M:%S"`','ss$i','$i','UP','log$i.txt','$i');" ;done

## Access Swagger for API
    $ http://127.0.0.1/swagger/


## Get auth0 account https://auth0.com/

-  Create a new application on auth0 and use theses values Domain, Client ID, Client Secret in docker-compose.yml
-  Default Connections should be "Username-Password-Authentication" 
-  Create API on auth0 and use API Audience value in docker-compose.yml
-  Create a new user on auth0 and Select permissions from existing APIs 


## Create a token to access the api
    $ curl -v --request POST --url 'http://127.0.0.1/auth0/v1' -H 'content-type: application/json' --data '{"username":"XXX","password": "XXX"}'

## Get all data 
    $ curl --request GET --url http://127.0.0.1/data/v1   --header 'authorization: Bearer TOKEN_GENERATED'


## Add new data 
    $ curl --request POST --url http://127.0.0.1/data/v1 --header 'Content-Type: application/json' --header 'authorization: Bearer TOKEN_GENERATED' --data '{"detailstatus": "Down","devicename": "ss1", "eventtime": "2019-04-21T00:33:47+00:00","filename": "log1.txt","id": "1631ea91-6e49-4aad-a699-d171d09f79c1","item": "1", "linenumber": 1}'

## Uptdate data
    $ curl --request PUT --url http://127.0.0.1/data/v1/1631ea91-6e49-4aad-a699-d171d09f79c1 --header 'Content-Type: application/json' --header 'authorization: Bearer TOKEN_GENERATED' --data '{"detailstatus": "Down","devicename": "ss1", "eventtime": "2019-04-21T00:33:47+00:00","filename": "log1.txt","item": "2", "linenumber": 1}'


## Delete data
    $ curl --request DELETE --url http://127.0.0.1/data/v1/1631ea91-6e49-4aad-a699-d171d09f79c1 --header 'Content-Type: application/json' --header 'authorization: Bearer TOKEN_GENERATED'
