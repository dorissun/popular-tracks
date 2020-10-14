# Tracks popularity using Spotify for Developers API

## Installation

make sure docker and docker-compose are installed

## To run

Fill in your Spotify Client ID and Client Secret in app/id_secret.json file and run:

```
docker-compose up --build
```

It starts 3 containers, the script itself, a mysql database and a simple database admin tool to be able to inspect the database in a browser.

The script fetches data about the tracks like name and popularity and exits. The database and admin tool keeps running. To quit, press ctrl-c.

The next day when you run `docker-compose up --build` it will fetch the latest popularity and add it to the database, so that you can track popularity over time.

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
