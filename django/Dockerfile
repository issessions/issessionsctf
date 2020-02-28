FROM python:3.6

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && apt-get install -y \
        python3-venv postgresql-client libpq-dev libldap2-dev libsasl2-dev ldap-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY . .

RUN if [ -f CA-key-and-cert/zentyal-samba-ca.crt ];then cp ./CA-key-and-cert/zentyal-samba-ca.crt /usr/local/share/ca-certificates/; \ 
	update-ca-certificates; fi

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

#RUN python3 -m venv ./venv && source ./venv/bin/activate

# Set date & time to Canada/Eastern
RUN cp /usr/share/zoneinfo/Canada/Eastern /etc/localtime

RUN chmod 700 /usr/src/app/django.sh
CMD ["/bin/bash", "-c", "bash /usr/src/app/django.sh"]
