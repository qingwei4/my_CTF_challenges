FROM ubuntu:22.04
MAINTAINER Terry1234

ENV DEBAIN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 xinetd

COPY flag /flag
COPY readflag /readflag

RUN chown root:root /flag && chmod 400 /flag
RUN chown root:root /readflag && chmod 4755 /readflag

RUN useradd -m ctf

USER ctf

CMD ["/usr/sbin/xinetd", "-dontfork"]