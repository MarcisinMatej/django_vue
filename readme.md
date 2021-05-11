# Django-vue Equity-market-cap project
Simple Django app with Vue front-end which will reguralry query API to get latest values for different equities.

The app is using redis, Celery for mesage management.
For the ease of development we use VUE with CDN instead of full installation. 


# Installation

Install python requirements as needed in the requiremnts file.
Install Redis or pull docker -> we use docker.
Start Redis
Start Django server

#### Runnig app in dev mode
Note, this app was developed on windows, however the command should be same for unix-based platforms.


```bash

#start redis db
docker run --name redis-django -p 6379:6379 -d redis
# move to project directory
cd emc_project

# you will need 3 terminal windows in this directory
# 1. terminal celery broker scheaduler
celery -A emc_project beat -l INFO
# 2. terminal celery worker
celery -A emc_project worker -l INFO

# 3. terminal django server
# colect static files
manage.py colect static
# start local server
manage.py runserver
```

#### Running app with docker
To ease usage a no need to use 3 different terminal windows the app was dockerized.
To start it you need to execute following command. Before running install docker, you can follow this page
https://docs.docker.com/get-docker/ 

```bash
docker-compose up --build
```

### Celery + Redis

Celery is library which manages workers.
Worker is a function which executes defined task (for example get latest value of some stock/crypto coind)
Task is definied in the Django project.
Django uses Broker to pass task to Celery.
Broker basically stores the task in specific data-structure.
When broker registers task, it puts it into the queue.
At the same time broker takes the tasks from queue and passes them to brokers.
Then Celery worker takes this tasks and puts result into the result back-end (also broker)
Then the Django can fetch it from queue.
For a broker we will use Redis.


### Consuming the messages
Given our solution we use Asynchronuous type of communication and for that we will use Channels-redis package
This part will be responsible for picking up the results and pushing them to the FE
For that we needed to define ASGI configs, like routings, consumers etc...