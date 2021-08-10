FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
