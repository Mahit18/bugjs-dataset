FROM node:8.16-stretch

RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list

RUN apt-get update && \
	apt-get install -y nano python3 screen zip unzip

RUN mkdir -p /work
WORKDIR /work
RUN npm i --save fs-extra@7.0.1
RUN npm i --save mkdirp@0.5.1
RUN npm i -g istanbul@0.4.5
RUN npm i -g n@2.1.12
RUN npm i -g grunt-cli@1.2.0
RUN npm i --save glob@7.1.6 

RUN echo '{ "allow_root": true, "registry": "https://registry.bower.io" }' > /root/.bowerrc

RUN echo 'loglevel = "error"' > /root/.npmrc

COPY profile /root/.bashrc

# Redis for node_redis
RUN wget http://download.redis.io/releases/redis-3.2.12.tar.gz && \
	tar xvzf redis-3.2.12.tar.gz && \
	cd redis-3.2.12 && \
	make && \
	cp src/redis-server /usr/local/bin/redis-server && \
	cp src/redis-cli /usr/local/bin/redis-cli && \
	cd .. && \
	rm -rf redis-3.2.12 && \
	rm redis-3.2.12.tar.gz


# Mongodb for mongoose
# 3.6
RUN wget -qO - https://www.mongodb.org/static/pgp/server-3.6.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/3.6 main" | tee /etc/apt/sources.list.d/mongodb-org-3.6.list
RUN apt-get update
RUN apt-get install -y --allow-unauthenticated mongodb-org
RUN rm /etc/apt/sources.list.d/mongodb-org-3.6.list

# 2.4, 2.6
RUN wget -qO- http://downloads.mongodb.org/linux/mongodb-linux-x86_64-2.4.14.tgz | tar zxfv - -C /opt
RUN wget -qO- http://downloads.mongodb.org/linux/mongodb-linux-x86_64-2.6.12.tgz | tar zxfv - -C /opt

RUN n 8.0.0

COPY work /work

RUN chmod +x /work/*

ARG CACHE_DATE=2018-07-20

RUN git clone https://github.com/nus-apr/bugjs-dataset.git /work/bugjs/

