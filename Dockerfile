FROM python:3.9-slim-buster
WORKDIR /app
COPY . .
RUN pip install pipenv
RUN pipenv install --dev --system

ENTRYPOINT "/bin/bash"
