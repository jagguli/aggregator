# Web scraper and aggregator
## API

To query scraped docs

```
curl http://localhost:8000/api/v1/articles/search/?q=test
```

To kick off a scrape job

```
curl http://localhost:8000/api/v1/articles/search/scrape/
```
## API Docs

API documentation is automatically generated using Swagger. You can view documention by visiting this [link](http://localhost:8000/swagger).

## Prerequisites

If you are familiar with Docker, then you just need [Docker](https://docs.docker.com/docker-for-mac/install/). If you don't want to use Docker, then you just need Python3 and Postgres installed.

## Local Development with Docker

Start the dev server for local development:

```bash
cp .env.dist .env
docker-compose up -d --remove-orphans --build
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```



## Local Development without Docker

### Install

```bash
pip install -U poetry & poetry install & poertry shell        # activate venv
cp .env.dist .env                                             # create .env file and fill-in DB info
./manage.py migrate                                           # run migrations
./manage.py collectstatic --noinput                           # collect static files
redis-server                                                  # run redis locally for celery
celery -A src.config worker --beat --loglevel=debug
  --pidfile="./celerybeat.pid"
  --scheduler django_celery_beat.schedulers:DatabaseScheduler # run celery beat and worker
```

### Run dev server

This will run server on [http://localhost:8000](http://localhost:8000)

```bash
./manage.py runserver
```

### Create superuser

If you want, you can create initial super-user with next commad:

```bash
./manage.py createsuperuser
```

### Running Tests

To run all tests with code-coverate report, simple run:


```bash
pytest -s src/scraper/
```
