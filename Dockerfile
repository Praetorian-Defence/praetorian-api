FROM python:3.12-slim as builder

# System setup
RUN apt update -y
RUN apt install -y libffi-dev build-essential libsasl2-dev libpq-dev libldap-dev libjpeg-dev zlib1g-dev
WORKDIR /usr/src/app

# https://github.com/python-ldap/python-ldap/issues/432
RUN echo 'INPUT ( libldap.so )' > /usr/lib/libldap_r.so

# Copy source
COPY . .

## Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Dependencies
RUN pip3 install --user gunicorn wheel --no-cache-dir
RUN pip3 install --user -r requirements.txt --no-cache-dir

FROM python:3.12-slim

RUN apt update -y
RUN apt install -y supervisor curl postgresql-client argon2 tzdata cron

WORKDIR /usr/src/app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/src/app /usr/src/app
ENV PATH=/root/.local/bin:$PATH

## Configuration
COPY conf/supervisor.conf /etc/supervisord.conf
RUN chmod +x conf/entrypoint.sh

# Health check
#HEALTHCHECK CMD curl --fail http://localhost:9000/api/v1/status || exit 1

# Execution
CMD ["conf/entrypoint.sh"]
