FROM python:3.12-slim-bullseye as prod

RUN pip install poetry==1.7.1

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main

WORKDIR /app/src/backend

CMD ["/usr/local/bin/python", "-m", "main"]