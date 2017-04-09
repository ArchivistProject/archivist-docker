FROM debian:unstable

ENV DEBIAN_FRONTEND=noninteractive

ADD syslog-stdout/ /tmp/src/syslog-stdout

RUN apt-get update -yq && apt-get upgrade -yq && \
    apt-get install -yq --no-install-recommends haproxy inotify-tools ca-certificates build-essential git libpcre3-dev golang curl && \
    cd / && \
    export GOPATH=/tmp && \
    go get github.com/ziutek/syslog && \
    go build syslog-stdout && \
    apt-get purge -yq --autoremove build-essential git libpcre3-dev golang && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    rm -rf /openssl-build /haproxy-build /usr/share/doc /usr/share/doc-base /usr/share/man /usr/share/locale /usr/share/zoneinfo && \
    haproxy -vv

RUN mkdir /etc/ssl/archivist
ADD certificates/cert.* /etc/ssl/archivist/

ADD docker_entrypoint.sh /
RUN chmod 777 docker_entrypoint.sh

ENTRYPOINT ["./docker_entrypoint.sh"]
