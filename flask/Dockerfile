
FROM python:3.7

WORKDIR /
COPY . .

RUN apt update -q;apt upgrade -yq
RUN apt install -yq golang gcc cron

#download for fallback 
RUN wget -N https://github.com/twbs/bootstrap/releases/download/v4.4.1/bootstrap-4.4.1-dist.zip
RUN unzip bootstrap-4.4.1-dist.zip
RUN rm bootstrap-4.4.1-dist.zip
RUN mkdir -p ./static
RUN mv ./bootstrap-4.4.1-dist ./static/bootstrap-4.4.1-dist
RUN wget -N https://code.jquery.com/jquery-3.4.1.min.js
RUN mkdir -p ./static/bootstrap-4.4.1-dist/js
RUN mv ./jquery-3.4.1.min.js ./static/bootstrap-4.4.1-dist/js/jquery-3.4.1.min.js

RUN pip install -U flask waitress janome werkzeug psutil urllib3 certifi
RUN go get github.com/mitchellh/go-ps
RUN go get github.com/mattn/go-sqlite3

#crontab
RUN echo "*/5 * * * * root go run nicoapi.go" > etc/cron.d/nicoapi.sh

CMD bash -c "waitress-serve --port=8080 wsgi:app;go run nicoapi.go"
#CMD python app.py
