import logging
from ctf.ldap_ops import LDAPOperator
from django_auth_ldap.backend import LDAPBackend
from django.core.management.base import BaseCommand, CommandError
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class Command(BaseCommand):
    help = 'Sync teams from the LDAP server to the Postgresql DB'
    def handle(self, *args, **options):
        ldap_object = LDAPOperator() 
        result_set = ldap_object.find_ldap_users("*")
        ldap_backend = LDAPBackend()
        target_group = b'CN=ctf-participant,CN=Groups,DC=ctf,DC=issessions,DC=ca'
        for entry in result_set:
            try:
                group_list = (entry[1]['memberOf'])
                if target_group in group_list:
                    ldap_backend.populate_user( entry[1]['sAMAccountName'][0].decode('UTF-8') )
            except:
                logging.debug("nothing happens...")

        