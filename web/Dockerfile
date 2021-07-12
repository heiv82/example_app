FROM python:3.8-alpine


COPY . /app
WORKDIR /app

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG True

RUN apk update && apk add alpine-sdk gcc musl-dev python3-dev libffi-dev openssl-dev cargo jpeg-dev zlib-dev ffmpeg linux-headers

RUN pip install -U pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run"]
