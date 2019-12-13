
FROM python:3.7

RUN mkdir -p /flask
WORKDIR /flask
COPY . .

RUN apt update -q;apt upgrade -yq
RUN apt install -yq golang gcc cron

RUN pip install -U pip
RUN pip install -U flask waitress janome werkzeug psutil urllib3 certifi
RUN go get github.com/mitchellh/go-ps
RUN go get github.com/mattn/go-sqlite3

RUN go build -o ./nicoapi.elf ./nicoapi.go

CMD bash -c "waitress-serve --port=8080 wsgi:app;./nicoapi.elf"
#CMD python app.py
