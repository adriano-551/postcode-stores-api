## Overview ##

This project was a way for me to learn some of the basics on setting up Flask using a Docker container, the json file exists as a stand in for a database that I may set up at a later date.

To run this project you need docker installed.

## Installation

Create the docker containers by running the following

`sudo bash start.sh`

Tests can be run by using the following

`docker exec -it docker.store-postcodes-api pytest`