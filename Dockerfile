FROM ghcr.io/anomalyco/opencode:2.1.3

WORKDIR /root

RUN apk add --no-cache git uv

RUN uv python install 3.13

ENTRYPOINT ["/bin/sh", "-c", "opencode serve"]
