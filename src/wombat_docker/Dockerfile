#
# docker build --build-arg WOMBAT_UID=$(id -u wombat) --build-arg WOMBAT_GID=$(id -g wombat) -t mastodon:latest -f src/wombat_docker/Dockerfile src/
# docker run -v /var/wombat:/mnt/wombat --name mastodon mastodon:latest
# docker run -e stuntbox=validator -v /var/wombat:/mnt/wombat --name mastodon mastodon:latest
# docker run -e stuntbox=scorer -e limit=5 --name mastodon mastodon:latest
# docker run -e stuntbox=scorer --name mastodon mastodon:latest
#
FROM python:3.11-slim

WORKDIR /app

# Require wombat UID/GID to be provided by the Linux build host.
ARG WOMBAT_UID
ARG WOMBAT_GID

RUN set -eux; \
	test -n "${WOMBAT_UID}"; \
	test -n "${WOMBAT_GID}"

RUN printf '%s\n' '#!/bin/sh' 'set -eu' \
	'uid="${WOMBAT_UID:?WOMBAT_UID is required}"' \
	'gid="${WOMBAT_GID:?WOMBAT_GID is required}"' \
	'printf "WOMBAT_UID=%s\nWOMBAT_GID=%s\n" "$uid" "$gid" > /app/wombat_env.env' \
	> /usr/local/bin/collect-wombat-ids.sh \
	&& chmod +x /usr/local/bin/collect-wombat-ids.sh

ENV WOMBAT_UID=${WOMBAT_UID}
ENV WOMBAT_GID=${WOMBAT_GID}

RUN /usr/local/bin/collect-wombat-ids.sh

# Create and activate virtualenv first
RUN python -m venv /app/venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install them inside the venv
COPY wombat_docker/requirements.txt ./
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt

COPY helper/ ./helper/
COPY wombat_docker/mastodon_app.py ./
COPY wombat_docker/koala.py ./
COPY wombat_docker/validator.py ./

RUN printf '%s\n' '#!/bin/sh' 'set -e' '/usr/local/bin/collect-wombat-ids.sh' 'set -a' '[ -f /app/wombat_env.env ] && . /app/wombat_env.env' 'set +a' 'exec "$@"' > /usr/local/bin/docker-entrypoint.sh \
	&& chmod +x /usr/local/bin/docker-entrypoint.sh

ENV FAILURE_DIR=/mnt/wombat/failure/
ENV FRESH_DIR=/mnt/wombat/fresh/mastodon
ENV KOALA_DIR=/mnt/wombat/mastodon/koala
ENV SUCCESS_DIR=/mnt/wombat/mastodon/success/

ENV DB_CONN=postgresql+psycopg2://mastodon_client:batabat@172.17.0.1:5432/mastodon

RUN mkdir -p /mnt/wombat
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "mastodon_app.py"]
