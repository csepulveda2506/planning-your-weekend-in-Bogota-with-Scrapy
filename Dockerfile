FROM python:3.6.1-alpine

RUN apk add --update --no-cache build-base linux-headers git cmake bash #wget mercurial g++ autoconf libgflags-dev cmake bash jemalloc libpq postgresql postgresql-dev postgresql-libs
RUN apk add --update --no-cache zlib zlib-dev bzip2 bzip2-dev snappy snappy-dev lz4 lz4-dev jemalloc jemalloc-dev

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .
