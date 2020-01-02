# pull official base image
FROM python:3.8.0-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME \
    && mkdir $APP_HOME/static \
    && mkdir $APP_HOME/media
WORKDIR $APP_HOME

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev zlib libjpeg-turbo-dev libpng-dev freetype-dev lcms2-dev libwebp-dev harfbuzz-dev fribidi-dev tcl-dev tk-dev\
    && pip install --upgrade pip \
    && pip install -r /usr/src/app/requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME
    

# change to the app user
USER app

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]