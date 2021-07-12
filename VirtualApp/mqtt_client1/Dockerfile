 
FROM python:3.9-alpine

RUN pip3 install --upgrade pip

COPY . /mqtt
WORKDIR /mqtt

ENV FLASK_DEBUG True

COPY requirements.txt requirements.txt

RUN apk update && apk add alpine-sdk gcc musl-dev python3-dev libffi-dev openssl-dev cargo jpeg-dev zlib-dev  ffmpeg

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .


CMD ["python", "-u", "main.py"]
 
 
