FROM python:3.7-slim-buster
RUN mkdir -p /var/auth-server
COPY ./ /var/auth-server
ADD odbcinst.ini /etc/odbcinst.ini
RUN apt-get update
RUN apt-get install -y gcc g++
RUN apt-get install -y tdsodbc unixodbc-dev --no-install-recommends apt-utils
RUN apt install unixodbc-bin -y --no-install-recommends apt-utils
RUN apt-get clean -y
RUN pip install -r /var/auth-server/requirements.txt
ENV auth_db_connection="Driver={xxx};Server=192.168.99.145;Database=xxx;Uid=xxx;Pwd=xxx;"

ENTRYPOINT python /var/auth-server/app.py
EXPOSE 8083