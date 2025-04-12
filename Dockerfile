FROM debian:bullseye-slim

LABEL maintainer="soda3x - https://github.com/soda3x"
LABEL org.opencontainers.image.source=https://github.com/soda3x/docker-reforger-server

ARG UID=1000
ARG GID=1000

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update \
    && \
    apt-get install -y --no-install-recommends --no-install-suggests \
    python3 \
    lib32stdc++6 \
    lib32gcc-s1 \
    wget \
    ca-certificates \
    libcurl4 \
    net-tools \
    libssl1.1 \
    wamerican \
    && \
    apt-get remove --purge -y \
    && \
    apt-get clean autoclean \
    && \
    apt-get autoremove -y \
    && \
    rm -rf /var/lib/apt/lists/* \
    && \
    mkdir -p /home/reforger \
    && \
    mkdir -p /home/reforger/steamcmd \
    && \
    wget -qO- 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz' | tar zxf - -C /home/reforger/steamcmd



ENV USE_EXPERIMENTAL=false
ENV CONFIG=""
ENV MAX_FPS=60
ENV MAX_RESTARTS=0
ENV FREEZE_CHECK=300
WORKDIR /home/reforger/reforger_bins

VOLUME /home/reforger/steamcmd
VOLUME /home/reforger/profile
VOLUME /home/reforger/configs
VOLUME /home/reforger/workshop

EXPOSE 2001/udp
EXPOSE 17777/udp
EXPOSE 19999/udp

STOPSIGNAL SIGINT

COPY *.py /

CMD ["python3","/launch.py"]
