FROM python:3.12-slim-bullseye as prod

# Install system-level dependencies
RUN apt-get update && apt-get install -y build-essential libffi-dev

# Upgrade pip
RUN pip install --upgrade pip


RUN pip install poetry==1.7.1

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock requirements.txt /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main
RUN pip install -r requirements.txt

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main
RUN pip install -r requirements.txt

WORKDIR /app/src/backend

CMD ["/usr/local/bin/python", "-m", "main"]