FROM python:3.7.1

SHELL ["/bin/bash", "-c"]

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
RUN python3 -m pip install -r requirements.txt

CMD gunicorn analysisapi.wsgi -b 0.0.0.0:8000 --log-file -
