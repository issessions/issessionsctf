"""
Django settings for issessionsctf project.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, LDAPGroupQuery
# from django.contrib.auth.models import User

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2^f+3@v7$v1f8yt0!se3-1t$5tlp+xm17=*gno_xoi&&9m#2a&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'ctf.apps.CtfConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'issessionsctf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'issessionsctf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'iss',
        'USER': 'issessions',
        'PASSWORD': 'issessions',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': 'localhost:11211',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

LOGOUT_REDIRECT_URL = '/'


# Baseline configuration

AUTH_LDAP_SERVER_URI = "ldap://ZENTYAL.issessions.ca/"

BASE_DN = "dc=issessions,dc=ca"
BIND_OU = "ou=applications"
BIND_DN = "cn=django django" + "," + BIND_OU + "," + BASE_DN
USER_SEARCH_OU = "ou=ctf"
GROUP_SEARCH_OU = "ou=ctf"
USER_SEARCH_DN = USER_SEARCH_OU + "," + BASE_DN
GROUP_SEARCH_DN = GROUP_SEARCH_OU + "," + BASE_DN
ACTIVE_USERS_GROUP_DN = "cn=ctf_active," + GROUP_SEARCH_DN
DISABLED_USERS_GROUP_DN = "cn=ctf_disabled," + GROUP_SEARCH_DN
CTF_STAFF_GROUP_DN = "cn=ctf_staff," + GROUP_SEARCH_DN
CTF_TEAMS_GROUP_DN = "cn=ctf_teams," + GROUP_SEARCH_DN

AUTH_LDAP_BIND_DN = BIND_DN
AUTH_LDAP_BIND_PASSWORD = "django"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    USER_SEARCH_DN, ldap.SCOPE_SUBTREE, "(sn=%(user)s)"
)
# Or:
# AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=users,dc=example,dc=com'

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    GROUP_SEARCH_DN,
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)",
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

# group restrictions

AUTH_LDAP_REQUIRE_GROUP = (
    LDAPGroupQuery(CTF_STAFF_GROUP_DN)
    | LDAPGroupQuery(CTF_TEAMS_GROUP_DN)
)

AUTH_LDAP_USER_QUERY_FIELD = 'username'

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "username": "sn",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "password": "password",
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": ACTIVE_USERS_GROUP_DN,
    "is_staff": CTF_STAFF_GROUP_DN,
    "is_superuser": CTF_STAFF_GROUP_DN,
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache distinguished names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 0

# TLS/SSL LDAP
AUTH_LDAP_START_TLS = True

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django_auth_ldap": {"level": "DEBUG", "handlers": ["console"]}},
}
