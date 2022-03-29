FROM node:17-alpine
# FROM node:16-bullseye-slim
WORKDIR /usr/src/app

COPY package*.json ./

RUN apk update
# RUN apt-get update
RUN apk add libxext-dev
RUN apk add npm
# RUN apt-get update 

RUN apk add libressl-dev

# RUN apt-get install libssl-dev openssl -y
# RUN apt-get install wget -y
RUN wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
RUN tar xzvf Python-3.10.4.tgz
RUN rm Python-3.10.4.tgz
RUN cd Python-3.10.4 && ./configure && make && make install
# RUN cd ..
# RUN rm -rf Python-3.10.4

RUN apt-get install python3-pip -y
RUN pip3 install mysql-connector-python
RUN pip3 install tabulate


COPY . .

CMD ["npm", "start"]