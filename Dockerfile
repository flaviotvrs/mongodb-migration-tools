FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.5 \
    python3-pip \
    python3-setuptools \
    wget \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://downloads.mongodb.com/compass/mongodb-mongosh_1.0.3_amd64.deb \
    && wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu1804-x86_64-100.4.1.deb \
    && apt-get update && apt-get install -y --no-install-recommends \
    ./mongodb-mongosh_1.0.3_amd64.deb \
    ./mongodb-database-tools-ubuntu1804-x86_64-100.4.1.deb \
    && \
    apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm ./mongodb-mongosh_1.0.3_amd64.deb ./mongodb-database-tools-ubuntu1804-x86_64-100.4.1.deb

COPY . /opt/migration-tools/
WORKDIR /opt/migration-tools/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]