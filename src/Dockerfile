# pull official base image
FROM python:3.10-slim

# set work directory
WORKDIR /usr/src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt requirements.txt

# install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# copy project
COPY . .
