
FROM python:3.7

WORKDIR /
COPY . .

RUN apt update -q;apt upgrade -yq
RUN apt install -yq golang gcc cron

RUN pip install -U pip
RUN pip install -U flask waitress janome werkzeug psutil urllib3 certifi
RUN go get github.com/mitchellh/go-ps
RUN go get github.com/mattn/go-sqlite3

CMD bash -c "waitress-serve --port=8080 wsgi:app;go run nicoapi.go"
#CMD python app.py
