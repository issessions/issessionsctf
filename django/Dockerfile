FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod 700 /usr/src/app/django.sh
CMD ["/bin/bash", "-c", "bash /usr/src/app/django.sh"]
