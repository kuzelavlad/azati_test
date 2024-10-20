# FASTAPI PROJECT

A RESTful API for a stock trading application.

## Local Development

### Start the Stack with Docker Compose

To start the development environment, run the following command:

```bash
docker compose up -d
````
## Access the API

Now you can open your browser and interact with these URLs:

	•	Backend, JSON-based web API based on OpenAPI: http://localhost/api/
	•	Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

## Check the Logs

To check the logs, run:
```bash
docker compose logs
```

## To check the logs of a specific service, add the name of the service, e.g.:
```bash
docker compose logs fastapi
```

## To migrate alembic
```bash
alembic upgrade head
```