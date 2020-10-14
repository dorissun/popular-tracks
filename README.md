# Tracks popularity using Spotify for Developers API

## Installation

make sure docker and docker-compose are installed

## To run

* fill in your Spotify Client ID and Client Secret in app/id_secret.json file
* run docker-compose command in where the docker-compose.yaml file locates

  docker-compose up --build

## To view mysql tables

http://localhost:8080/  in the browser

Specify the following to login
System: Mysql
Server: db
Username: user
Password: 123
Database: test

Click "Select data" to view tracks and track_popularity tables in test db

Examples
