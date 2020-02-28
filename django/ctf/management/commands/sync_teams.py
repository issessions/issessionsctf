import logging
from django_auth_ldap.backend import LDAPBackend
from ctf.ldap_ops import LDAPOperator
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Sync teams from the LDAP server to the Postgresql DB'
    def handle(self, *args, **options):
        ldap_object = LDAPOperator() 
        result_set = ldap_object.find_ldap_teams()
        logging.debug(result_set)
