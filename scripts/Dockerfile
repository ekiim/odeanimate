FROM python:3.11
RUN apt-get update
RUN apt-get install --assume-yes texlive ffmpeg git
RUN pip install pipenv
WORKDIR /app
COPY Pipfile.lock Pipfile.lock
COPY ./scripts/install-dev-deps.sh ./scripts/install-dev-deps.sh
RUN ./scripts/install-dev-deps.sh
COPY . .
RUN pip install -e .
ENTRYPOINT "/bin/bash"
