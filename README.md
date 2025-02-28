# Track Visualization Project

This project allows you to upload track files, view them on a map, and interact with the data via an API. It uses Django for the backend, Dash for the frontend, and PostgreSQL for data storage.

## Technologies
- Django (for the backend)
- Dash (for the frontend)
- PostgreSQL (for the database)
- Docker (for containerization)

## Project Structure

- `backend/` - Code for the Django backend.
- `frontend/` - Code for the Dash frontend.
- `docker-compose.yml` - Configuration for running the services with Docker.
- `.env` - Environment variables for configuring the project (e.g., for the database).

## How to Run

Clone this repository

### Step 1

Rename `.env.sample` to `.env`

### Step 2
Use next command for run project:

```bash
docker-compose up --build
```
### Step 3
Dash application will be availabla by `127.0.0.1:8050`

API will be avaliable by `127.0.0.1:8000`

## Documentation

Swagger documentation will be available by `127.0.0.1:8000/api/schema/swagger/`
