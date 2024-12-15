FROM python:3.14-rc-slim-bullseye

# install dependencies 
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 
# Create a working directory
WORKDIR /mindspark
# Install dependencies
COPY requirement.txt requirement.txt
RUN pip install -U setuptools
RUN python -m pip install -r requirement.txt
COPY . /mindspark/
