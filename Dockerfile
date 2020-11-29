FROM ubuntu:18.04
# ARG SERVER_ENV=''
WORKDIR /src/fms-python-service-dev
COPY . .
# COPY app/env/$SERVER_ENV.env app/env/.env
RUN rm -rf appenv/
RUN apt-get update
RUN apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
RUN apt-get install -y python3-venv
RUN python3 -m venv appenv
RUN . appenv/bin/activate
RUN pip3 install -r requirements.txt
CMD uwsgi --socket 0.0.0.0:2100 --protocol=http -w wsgi:app
EXPOSE 2100
