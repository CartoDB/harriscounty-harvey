FROM python:2.7

RUN \
        echo 'deb http://http.us.debian.org/debian sid main non-free contrib' > /etc/apt/sources.list.d/sid.list \
        && apt-get update && apt-get install -y --no-install-recommends \
                gdal-bin/sid \
        && pip install --no-cache awscli \
        && rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]
