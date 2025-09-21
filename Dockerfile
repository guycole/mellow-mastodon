#
# mastodon collection processing csv2json.py
#
# docker build -t csv2json:1.0 .
# docker run -d --rm -v /var/mellow:/var/mellow csv2json:1.0
#
FROM python:3.12-bookworm
#
LABEL BUILD_DATE="2025-09-19"
LABEL DESCRIPTION="mellow mastodon collection processing"
LABEL MAINTAINER="guycole@gmail.com"
LABEL PROJECT="mellow-mastodon"
LABEL VERSION="1.0"
#
RUN apt-get update && apt-get install -y
#
RUN mkdir -p /var/mellow
#
WORKDIR /mellow/mastodon
#
COPY src/collector/csv2json.py .
COPY src/collector/power_file_epoch.py .
COPY src/collector/power_file_helper.py .
COPY src/collector/power_file_row.py .
COPY src/collector/power_file.py .
COPY src/collector/requirements.txt .
#
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
#
ENTRYPOINT [ "python3", "csv2json.py", "/var/mellow/mastodon/config.docker"]
#
