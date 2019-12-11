
FROM python:3.7

WORKDIR /
COPY . .

RUN pip install -r requirements.txt

RUN wget -N https://github.com/twbs/bootstrap/releases/download/v4.4.1/bootstrap-4.4.1-dist.zip
RUN unzip bootstrap-4.4.1-dist.zip
RUN rm bootstrap-4.4.1-dist.zip
RUN mv ./bootstrap-4.4.1-dist ./static/bootstrap-4.4.1-dist
RUN wget -N https://code.jquery.com/jquery-3.4.1.min.js
RUN mv ./jquery-3.4.1.min.js ./static/bootstrap-4.4.1-dist/js/jquery-3.4.1.min.js

CMD waitress-serve --port=8080 wsgi:app
#CMD python app.py
