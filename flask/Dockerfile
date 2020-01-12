
#FROM python:3.7
FROM ubuntu:19.10

RUN mkdir -p /flask
WORKDIR /flask
COPY . .

RUN apt update -q;apt upgrade -yq
RUN apt install -yq gcc
RUN apt install -yq python3 python3-pip mysql-server

RUN pip3 install -U pip
RUN pip3 install -U flask waitress janome werkzeug psutil urllib3 certifi pytz neologdn \
firebase-admin google-cloud-firestore google-cloud-storage BeautifulSoup4 requests urllib3 \
mysqlclient SQLAlchemy

CMD bash -c "waitress-serve --host=0.0.0.0 --port=8080 wsgi:app"
#CMD python app.py
