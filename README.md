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


## Running Tests

To run all tests with code-coverate report, simple run:

```bash
docker-compose exec web bash
pytest -s src/scraper/
```
