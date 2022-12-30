#DOCKERFILE: contains all the commands a user could call on cmd line to assemble an image

FROM python:3.10-slim-buster

# Do not cache Python packages
ENV PIP_NO_CACHE_DIR=yes

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# set PYTHONPATH to point to working directory
ENV PYTHONPATH "${PYTHONPATH}:/code/"

# Initializing new working directory
WORKDIR /code

# Transferring the code and essential data
COPY xetra ./xetra
COPY Pipfile ./Pipfile
COPY Pipfile.lock ./Pipfile.lock
COPY run.py ./run.py

RUN pip install pipenv
RUN pipenv install --ignore-pipfile --system