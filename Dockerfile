
FROM python:3.12.3-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt


COPY . .

EXPOSE 8000

# CMD gunicorn 'online_assignment_management.wsgi' --bind=0.0.0.0:8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
