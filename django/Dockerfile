FROM python:3.6

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y \
        python3-venv postgresql-client libpq-dev libldap2-dev libsasl2-dev ldap-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN chmod 700 /usr/src/app/django.sh
CMD ["/bin/bash", "-c", "bash /usr/src/app/django.sh"]
