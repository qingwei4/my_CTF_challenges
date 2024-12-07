FROM ubuntu:20.04
MAINTAINER Terry1234

RUN apt-get update && \
    DEBAIN_FRONTEND=noninteractive apt-get install -qy xinetd

RUN useradd -m note
RUN chown -R root:root /home/note
RUN chmod -R 755 /home/note

CMD ["/usr/sbin/xinetd", "-dontfork"]
