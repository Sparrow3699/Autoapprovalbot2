FROM python:alpine

ENV DEBIAN_FRONTEND="noninteractive"
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add --upgrade --no-cache bash ca-certificates git && \
    apk add --upgrade --no-cache --virtual builddeps g++ libffi-dev && \
    pip3 install --upgrade --no-cache-dir pip \
                                        aiofiles \
                                        motor \
                                        pymongo \
                                        pyrogram \
                                        tgcrypto \
                                        uvloop && \
    apk del builddeps && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp*

SHELL ["/bin/bash", "-c"]

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY . .

CMD ["bash", "start.sh"]