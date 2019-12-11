
FROM python:3.7

WORKDIR /
COPY . .

RUN pip install -r requirements.txt

CMD waitress-serve --port=8080 wsgi:app
#CMD python app.py
