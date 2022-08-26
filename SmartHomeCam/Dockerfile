#FROM python:3.8.0-alpine
#
#WORKDIR /usr/src/app
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
##RUN apk update
##RUN apk add mariadb-dev gcc python3-dev musl-dev zlib-dev jpeg-dev
##
#RUN apk add --update-cache
#RUN apk add --update alpine-sdk && apk add libffi-dev openssl-dev && apk --no-cache --update add build-base
#RUN apk add mariadb-dev gcc python3-dev musl-dev zlib-dev jpeg-dev
#
#
#RUN apk add --no-cache mariadb-connector-c-dev
#RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base
#
#
#COPY requirements.txt /usr/src/app/requirements.txt
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#
#
#COPY . /usr/src/app/
#
##RUN pip install --upgrade pip
##RUN pip install -r requirements.txt

FROM python:3.8-slim-bullseye

WORKDIR /usr/src/app

RUN apt-get -y update
RUN pip install --upgrade setuptools
RUN apt-get install -y libmariadb-dev
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS


COPY . /usr/src/app/
RUN cd /usr/src/app/ && \
    pip3 install -r requirements.txt


# Add pip3 install opencv-python==4.1.2.30 if you want to run the live webcam examples
