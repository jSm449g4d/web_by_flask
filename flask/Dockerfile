
FROM python:3.7

RUN mkdir -p /flask
WORKDIR /flask
COPY . .

RUN apt update -q;apt upgrade -yq
RUN apt install -yq gcc

RUN pip install -U pip
RUN pip install -U flask waitress janome werkzeug psutil urllib3 certifi

CMD bash -c "waitress-serve --port=8080 wsgi:app"
#CMD python app.py
