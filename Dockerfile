FROM python:alpine3.12

WORKDIR /scrapper

ADD . /scrapper

RUN apk --no-cache add gcc musl-dev

RUN pip3 install -r requirements.txt


CMD [ "python", "run.py" ]
