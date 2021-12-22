# Introduction

TODO

# Running locally

For your convenience, a docker image has been prepared. Application requires a database to function properly,
though, so we're gonna need to set up some local MySQL server for development purposes. Let's use dockerhub for that.

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

## Running the web application

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

To run selenium integration tests:

```
$ docker run -it -p 5000:5000 -v /path/to/repo:/app share-my-notes-image:1.0 /bin/bash
$ cd /app
$ source /opt/share_my_notes_venv/bin/activate
(share_my_notes_venv) $ python -m unittest discover test/web_app/ui
```

**TODO** integration test has problems with killing the python web app, pkill has to be done manually =(

# Tech debt todo-list

1. Preferably use react rather than the old-school angularjs (not feeling too comfortable with it yet,
   though and additionally would prefer to choose node for the backend rather than python in such case).
2. Take care of possible password leaks, definitely remove 'get all sessions' endpoint and rather than that
   expose some 'does session exist' endpoint.
3. Modularize the huge index.html (either as flask templates or angular templates, does not matter).
4. Add type annotations to python modules.
5. Apply black.
6. Create base docker image w/o sources copied for dev purposes. Remove dev-dependencies for deployment (eg. black or geckodriver).
7. Somehow take care of migrations in the future...
8. Get rid of CDN scripts, host them yourself.
9. Add more tests.
10. Add CI (checking black, pylint, mypy, running tests, bumping staging image on merge to develop)
11. Add logger rather than prints.
12. Possibly extract some logic from the API modules and move it closer to the persistence/data access layer.

# Missing functionalities

1. Synchronizing notes/concurrency. Right now editing by two users at the same time is gonna end with a car crash. Need to add some
   blocking mechanism and real-time synchronization, for instance via web sockets. Or at least poll sessions which
   are not being edited and refresh from the client.
2. Expiration of the notes is not being handled =( User can set it, but when retrieving notes the expired ones are also being returned.
3. Removal of the notes is not implemented.
4. WYSIWYG editor and unicode for the notes!

# Additional features worth implementing

1. Downloading notes (eg. ZIP file with all of the notes in txt format).
2. Sharing only selected notes rather than whole sessions.
3. Restoring session's password somehow (for example via email).
