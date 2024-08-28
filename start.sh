#!/bin/bash
docker build -t docker.store-postcodes-api .
docker run -d -p 56733:80 --name=docker.store-postcodes-api \
    -v $PWD:/store-postcodes-api -w /store-postcodes-api docker.store-postcodes-api
