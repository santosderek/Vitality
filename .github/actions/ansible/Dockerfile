FROM  ubuntu:latest

RUN apt install python3-pip -y \
    && pip3 install docker

COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["bash","/entrypoint.sh"]
