FROM python:latest

# fix the timezone asking when creating the container
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install necessery packages
RUN \
    apt-get update \
    && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*

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

# config nginx
# copy config
COPY ./container/nginx_app_site_config /etc/nginx/sites-available/app
# enable server block
RUN ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/

# listen on port
EXPOSE 80/tcp

# run on startup
ENTRYPOINT gunicorn --workers 3 --bind unix:/app/airodor_web_app/airodor_web_app/app.sock -m 777 wsgi:app
    