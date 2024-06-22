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


