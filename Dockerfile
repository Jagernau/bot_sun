FROM python:3.10
COPY . /system_monitorin_connect
WORKDIR /system_monitorin_connect

ENV TOKEN=${TOKEN}
ENV GROUP_ID=${GROUP_ID}
ENV DB_HOST=${DB_HOST}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_DB_NAME=${MYSQL_DB_NAME}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}
ENV MYSQL_PORT=${MYSQL_PORT}

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
