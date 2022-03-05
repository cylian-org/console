###
### Console
###
FROM alpine:latest

### Maintener
LABEL maintainer="Cylian Lab <contact+docker@cylian.org>"

### Install tools
RUN apk add --no-cache \
    python3 \
    py3-yaml

### Install console
COPY \
    config \
    core \
    console.py \
    /usr/local/console/
