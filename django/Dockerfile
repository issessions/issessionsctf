FROM python:3.7

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y \
        python3-venv postgresql-client libpq-dev libldap2-dev libsasl2-dev ldap-utils \
    && rm -rf /var/lib/apt/lists/*

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

RUN if [ -f CA-key-and-cert/zentyal-samba-ca.crt ];then cp ./CA-key-and-cert/zentyal-samba-ca.crt /usr/local/share/ca-certificates/; \ 
	update-ca-certificates; fi

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt
RUN cp /usr/share/zoneinfo/America/Toronto /etc/localtime

CMD ["gunicorn", "issessionsctf.wsgi:application", "--workers=5", "-b", "0.0.0.0:80"]
