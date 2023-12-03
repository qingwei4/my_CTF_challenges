FROM ubuntu:20.04
MAINTAINER Terry1234

RUN apt-get update && \
    DEBAIN_FRONTEND=noninteractive apt-get install -qy xinetd

RUN useradd -m gift
RUN chown -R root:root /home/gift
RUN chmod -R 755 /home/gift

CMD ["/usr/sbin/xinetd", "-dontfork"]
