# Text Annotation Thesis

## Run with Docker

Install Docker Desktop, then run from the repository root:

```bash
cp .env.example .env
docker compose up --build
```

Open the frontend at <http://localhost:8088>. The Django API is available at
<http://localhost:8000>, and the Socket.IO server listens on port `3001`.

The backend applies existing Django migrations automatically on startup. To
create an administrator account, run:

```bash
docker compose exec backend python manage.py createsuperuser
```

Stop the stack with `docker compose down`. To also delete PostgreSQL, Redis,
and uploaded-media volumes, use `docker compose down -v`.

Add your OpenAI key to the root `.env` file only if the LLM features are needed.
Never commit that file.

## Run without Docker

Navigate to backend directory using "cd backend"

Create your virtual environment and activate (On MacOs: python3 -m venv venv
source ./venv/bin/activate)

RUN "pip install -r requirements.txt" to install all dependencies

RUN migrations by typing "python manage.py makemigrations" and shortly after, "python manage.py migrate"

START the server by executing command "python manage.py runserver"


CELERY
start celery task using "celery -A backend.celery worker --loglevel=INFO"


REDIS
start redis server "redis-server"


FORNTEND
Navigate to backend directory using "cd texnnotationFrontend"

