# College Assignment Management System

This is a comprehensive website created using Python and django.



![screenshot-1](https://github.com/user-attachments/assets/e0e3fac3-5421-4cea-bfa4-e4382845ac8a)


![screenshot-2](https://github.com/user-attachments/assets/54141729-cc3e-4bd4-9a17-27c22ce6fcde)


![screenshot-3](https://github.com/user-attachments/assets/9e666d02-60ae-4ed0-83c5-ce3413436ecf)


![screenshot-4](https://github.com/user-attachments/assets/45f616c9-1f8c-4ace-a496-d8f79f11cf4b)


![screenshot-5](https://github.com/user-attachments/assets/04ccd1c6-6887-4ccd-b9db-9ae88ab89c44)

# To Run the app using Docker

## Prerequisites

* Docker
* Docker Compose

## Setup

Clone the repository:

```bash
git clone https://github.com/Ameen6789/college-assignment-management-system.git
cd college-assignment-management-system
```

Create a `.env` file in the project root and add the required environment variables.

Example:

```env

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

PRODUCTION=False
```

## Start the Application

Build and start the containers:

```bash
docker compose --build
docker compose up
```

To run in the background:

```bash
docker compose up --build -d
```



## Create a Superuser

```bash
docker compose exec api python manage.py createsuperuser
```

## View Logs

```bash
docker compose logs -f
```

For a specific service:

```bash
docker compose logs -f api
```

## Stop Containers

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down -v
```

**Warning:** `docker compose down -v` deletes PostgreSQL data stored in Docker volumes.

## Development Mode

If Docker Compose watch mode is configured:

```bash
docker compose watch
```

or

```bash
docker compose up --watch
```

File changes will be synchronized into the running container automatically.

## Production

Set:

```env
PRODUCTION=True
```

When `PRODUCTION=True`:

* Media files are stored in Amazon S3.
* Static files are served using WhiteNoise.
* Production AWS environment variables must be configured.

