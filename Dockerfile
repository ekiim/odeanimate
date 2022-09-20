FROM python:3.7-slim
RUN apt-get update
RUN apt-get install --assume-yes texlive ffmpeg
RUN pip install poetry
RUN poetry config virtualenvs.create false
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi
COPY . .
RUN pip install -e .
ENTRYPOINT "/bin/bash"
