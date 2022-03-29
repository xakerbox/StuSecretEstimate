FROM alpine
# FROM node:16-bullseye-slim
RUN apk add --update nodejs npm

WORKDIR /app

COPY package*.json ./

RUN apk update
# RUN apt-get update
RUN apk add libxext-dev libressl-dev zlib-dev
# RUN apk add npm
# RUN apt-get update 

# RUN apk add libressl-dev
# RUN apk add zlib-dev

# RUN apt-get install libssl-dev openssl -y
# RUN apt-get install wget -y

RUN apk add --update alpine-sdk
# RUN apk add gcc libc-dev make
RUN wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
RUN tar xzvf Python-3.10.4.tgz
RUN rm Python-3.10.4.tgz
RUN cd Python-3.10.4 && ./configure && make && make install && cd .. && rm -r Python-3.10.4
# RUN cd ..
# RUN rm -rf Python-3.10.4

RUN apk add py3-pip
RUN pip install mysql-connector-python
RUN pip install tabulate

RUN npm ci
COPY . .

# ENV PORT 4200
# EXPOSE $PORT
VOLUME ["/app"]

CMD ["npm", "start"]