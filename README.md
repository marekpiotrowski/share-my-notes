# Introduction

TODO

# Running locally

For your convenience, a docker image has been prepared. Application requires a database to function properly,
though, so we're gonna need to set up some local MySQL server for development purposes. Let's use dockerhub for that, though.

## Preparing the database

```
$ docker pull mysql
$ docker run --name share-my-notes-db -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
$ docker exec -i share-my-notes-db mysql -P3306 -uroot -pmy-secret-pw < create_database.sql
```

To construct the connection string, we're gonna need the db's container IP address:

```
$ docker inspect share-my-notes-db | grep \"IPAddress\"
```

In my case it was `172.17.0.2`, so the connection string is gonna look like this:

```
$ export DB_CONNECTION_STRING="mysql+pymysql://root:my-secret-pw@172.17.0.2/share_my_notes_db?charset=utf8mb4"
```

## Running the web Application

Let's start with building the image and then starting the container. Assuming you're in the repository's root:

```
$ docker build --tag share-my-notes-image:1.0 .
$ docker run --env DB_CONNECTION_STRING=mysql+pymysql://root:my-secret-pw@172.17.0.2/share_my_notes_db?charset=utf8mb4 -p 5000:5000 share-my-notes-image:1.0
```

And that's it. In your command prompt, you should see something like that:

```
Running on http://172.17.0.3:5000/ (Press CTRL+C to quit)
```

Simply navigate there in your browser and you shall see the home page of Share My Notes app.

**For local development it's more convenient to map the repository as a volume when starting the container rather than using the copied sources, obviously:**
```
$ docker run --env DB_CONNECTION_STRING=mysql+pymysql://root:my-secret-pw@172.17.0.2/share_my_notes_db?charset=utf8mb4 -it -p 5000:5000 \
  -v /path/to/repo:/app share-my-notes-image:1.0 /bin/bash
```

# Running tests

To run the backend (kinda unit) tests, let's start the container interactively:

```
$ docker run -it -p 5000:5000 -v /path/to/repo:/app share-my-notes-image:1.0 /bin/bash
$ cd /app
$ source /opt/share_my_notes_venv/bin/activate
(share_my_notes_venv) $ python -m unittest discover test/data_access_layer
(share_my_notes_venv) $ python -m unittest discover test/web_app/api
```

To run selenium integration test:

```
$ docker run -it -p 5000:5000 -v /path/to/repo:/app share-my-notes-image:1.0 /bin/bash
$ cd /app
$ source /opt/share_my_notes_venv/bin/activate
(share_my_notes_venv) $ python -m unittest discover test/web_app/ui
```

**TODO** integration test has problems with killing the python web app, pkill has to be done manually =(
