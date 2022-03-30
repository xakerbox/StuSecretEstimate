# FROM alpine
FROM node:16-bullseye
# RUN apk add --update nodejs npm

WORKDIR /app

COPY package*.json ./

RUN apt-get update

# RUN npm install
RUN apt-get update 

RUN apt-get install libssl-dev openssl -y
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
RUN python3 -m pip install PyMySQL
RUN pip3 install fpdf2

RUN npm install

COPY . .

# ENV PORT 4200
# EXPOSE $PORT
VOLUME ["/app"]

CMD ["npm", "start"]