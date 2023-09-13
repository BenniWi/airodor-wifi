FROM python:latest

# prepare python
RUN pip3 install poetry gunicorn

# copy application
RUN mkdir /app 
COPY ./airodor_wifi_api/ /app/airodor_wifi_api
COPY ./airodor_web_app/ /app/airodor_web_app

WORKDIR /app/airodor_web_app/airodor_web_app

# prepare poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

# listen on port
EXPOSE 80/tcp

# run on startup
ENTRYPOINT gunicorn --workers 2 --bind 0.0.0.0:80 wsgi:app