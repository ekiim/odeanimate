FROM python:3.9-slim
WORKDIR /app
COPY odeanimate/__init__.py odeanimate/__init__.py
RUN apt-get update
RUN apt-get install --assume-yes texlive ffmpeg
RUN pip install pipenv
COPY odeanimate odeanimate
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY setup.py setup.py
COPY pyproject.toml pyproject.toml
COPY README.md README.md
RUN pipenv install --dev --system
COPY . .
ENTRYPOINT "/bin/bash"
