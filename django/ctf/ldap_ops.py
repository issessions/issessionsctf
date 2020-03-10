import ldap
import ldap.modlist as modlist
import sys
import logging
from issessionsctf.settings import AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD, \
    USER_SEARCH_DN, CTF_STAFF_GROUP_DN, CTF_TEAMS_GROUP_DN, ACTIVE_USERS_GROUP_DN, DISABLED_USERS_GROUP_DN, GROUP_SEARCH_DN, TEAM_SEARCH_DN
from ctf.models import Challenge, Submission, Team, Flag, Sponsorship, Sponsor,Contest
from django.contrib.auth.models import User



OBJECT_CLASS_USER_SCHEMA = [b'top', b'posixAccount', b'person', b'systemQuotas',
                            b'organizationalPerson', b'user']


class LDAPOperator:

    def __init__(self, bind_dn=AUTH_LDAP_BIND_DN, bind_password=AUTH_LDAP_BIND_PASSWORD):

        logging.basicConfig(level=logging.DEBUG)

        try:
            self.l = ldap.initialize(AUTH_LDAP_SERVER_URI, trace_level=2, trace_file=sys.stdout)
            logging.debug("LDAP: {0}".format("Successfully Initialized LDAP Object"))
            self.l.bind_s(who=bind_dn, cred=bind_password, method=ldap.AUTH_SIMPLE)
            logging.debug("LDAP: {0}".format("Successfully Authenticated to LDAP Server"))
        except ldap.LDAPError as le:
            logging.debug('LDAP Error: {0}'.format(le))
        except Exception as e:
            logging.debug('Error: {0}'.format(e))

        logging.debug("LDAP Version: {0}".format(self.l.protocol_version))
        logging.debug("TLS Available: {0}".format(ldap.TLS_AVAIL))

    def find_ldap_users(self,cn_to_find):
        try:
            results = self.l.search_s(USER_SEARCH_DN, ldap.SCOPE_SUBTREE, filterstr=("cn="+cn_to_find), attrlist=['sAMAccountName','memberOf'])#
            logging.debug("searched for user")
            return results
        except ldap.LDAPError as le:
            logging.debug('LDAP Error: {0}'.format(le))
        except Exception as e:
            logging.debug('Error: {0}'.format(e))


    def find_ldap_teams(self):
        try:
            # This is the LDAP query that gets all the teams and their members
            results = self.l.search_s(TEAM_SEARCH_DN, ldap.SCOPE_SUBTREE, filterstr="CN=*", attrlist=['member'])
            # For all the teams in the list of teams
            for team_num in range(0,len(results)):
                # split the elements of the team into a LIST
                team_elements = str(results[team_num]).split(',')
                # take only the name of the team i.e. cut out some random LDAP cruft
                team_name = team_elements[0][5:]
                # Try to get the team out of the database,
                # if it works it means the team is already in there
                try:
                    current_team = Team.objects.get(name=team_name)
                except:
                    current_team = None   

                #put the team in the database if it isn't already in there                 
                if(current_team == None):
                    current_team = Team(name=team_name,contest=Contest.objects.get(name='ctf2020'),active=True)
                    current_team.save()     
                # for every user that is a member of that team, get their sAMAccountName out of the LDAP and use it to 
                # get their name user object and put it in the memebers field of the Database           
                for member_num in range( 0,len(results[team_num][1]['member'])):
                    member_info = str(results[team_num][1]['member'][member_num]).split(',')
                    member_cn = member_info[0][5:]
                    user_result = self.find_ldap_users(member_cn)
                    db_username = str(user_result[0][1]['sAMAccountName'][0])
                    db_username = db_username[2:len(db_username)-1]
                    user_to_add = User.objects.get(username=str(db_username))
                    if user_to_add in current_team.members.all():
                        #don't add the user because they are already there
                        pass
                    else:
                        current_team.members.add(user_to_add)
            return results
        except ldap.LDAPError as le:
            logging.debug('LDAP Error: {0}'.format(le))
        except Exception as e:
            logging.debug('Error: {0}'.format(e))


#     def create_ldap_user(self, first_name, last_name, email, password, description):
#         try:

#             results = self.l.search_s(USER_SEARCH_DN, ldap.SCOPE_SUBTREE, filterstr="sn=*", attrlist=['uidNumber'])
#             lastUidNumber = int(max([result[1]['uidNumber'][0].decode('utf-8') for result in results]))

#             username = generate_username(first_name, last_name)

#             dn = "cn=" + username + "," + USER_SEARCH_DN

#             attrdict = {
#                 'objectclass': OBJECT_CLASS_USER_SCHEMA,
#                 'uidNumber': str(lastUidNumber + 1).encode('utf-8'),
#                 'cn': username.encode('utf-8'),
#                 'givenName': first_name.encode('utf-8'),
#                 'displayName': username.encode('utf-8'),
#                 'sn': last_name.encode('utf-8'),
#                 'sAMAccountName': username.encode('utf-8'),
#                 'mail': email.encode('utf-8'),
#                 'description': description.encode('utf-8'),
#                 'userAccountControl': b'513',
#                 #'memberOf': [ACTIVE_USERS_GROUP_DN.encode('utf-8'), CTF_TEAMS_GROUP_DN.encode('utf-8')],
#                 'userPassword': password.encode('utf-8'),
#                 'quota': b'500',
#                 'homeDrive': b'H:',
#                 'homeDirectory': ("\\\\zentyal.ISSESSIONS.CA\\" + username).encode('utf-8')
#             }

#             prettyattr = ldap.modlist.addModlist(entry=attrdict)

#             self.l.add_s(dn=dn, modlist=prettyattr)

#             # self.l.passwd_s(user=dn, oldpw='', newpw='heybaby')

#         except ldap.ALREADY_EXISTS as ae:
#             logging.debug('LDAP Error: {0}'.format(ae))
#         except ldap.LDAPError as le:
#             logging.debug('LDAP Error: {0}'.format(le))
#         except Exception as e:
#             logging.debug('Error: {0}'.format(e))

#     def delete_ldap_user(self, dn):
#         try:
#             pass
#         except ldap.LDAPError as le:
#             logging.debug('LDAP Error: {0}'.format(le))
#         except Exception as e:
#             logging.debug('Error: {0}'.format(e))


# def generate_username(first_name, last_name):
#     first_name = ''.join(filter(str.isalpha, first_name))
#     last_name = ''.join(filter(str.isalpha, last_name))
#     username = first_name[0:min(len(first_name), 5)] + last_name[0]
#     return username


def generate_group_membership(is_active, is_ctf_team, is_ctf_admin):

    if is_ctf_team and is_ctf_admin:
        return None

    member_of = []

    if is_active:
        member_of.append(ACTIVE_USERS_GROUP_DN)
    else:
        member_of.append(DISABLED_USERS_GROUP_DN)

    if is_ctf_admin:
        member_of.append(CTF_STAFF_GROUP_DN)

    if is_ctf_team:
        member_of.append(CTF_TEAMS_GROUP_DN)

    return member_of


#if __name__ == '__main__':
#    l = LDAPOperator()
#    l.create_ldap_user(first_name='brie', last_name='cheddar', email='majd@gmail.com', password='abc123',
#                       description='my youngest brother')
    # l.find_ldap_user()
