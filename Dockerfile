
FROM python:3.6-alpine

WORKDIR /abc

ENV BUILD_LIST git

RUN apk add --update $BUILD_LIST \
    && git clone https://github.com/leesander1/ABC.git /abc \
    && apk --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --update add leveldb leveldb-dev \
    && pip install pipenv \
    && pipenv --python=python3.6 \
    && pipenv install \
    && apk del $BUILD_LIST \
    && rm -rf /var/cache/apk/*

EXPOSE 5000

ENTRYPOINT [ "pipenv", "run", "python", "/abc/main.py" ]