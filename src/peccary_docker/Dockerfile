#
# Build from the src/ directory (one level above this file):
# docker build -f peccary_docker/Dockerfile -t peccary:latest .
# docker run -v /var/peccary:/mnt/peccary --name peccary peccary:latest
#
FROM python:3.11-slim

WORKDIR /app

# Create and activate virtualenv first
RUN python -m venv /app/venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements and install them inside the venv
COPY peccary_docker/requirements.txt ./
RUN $VIRTUAL_ENV/bin/pip install --no-cache-dir -r requirements.txt

COPY helper/ ./helper/
COPY peccary_docker/mastodon_app.py ./
COPY peccary_docker/loader.py ./

ENV FAILURE_DIR=/mnt/peccary/mastodon/failure
ENV FRESH_DIR=/mnt/peccary/mastodon/mastodon-v2

# On Linux (production): override with -e DB_CONN=...@172.17.0.1:5432/heeler
# On macOS (Docker Desktop): host.docker.internal resolves to the host machine
ENV DB_CONN=postgresql+psycopg2://mastodon_client:batabat@host.docker.internal:5432/mastodon

RUN mkdir -p /mnt/peccary
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "mastodon_app.py"]
