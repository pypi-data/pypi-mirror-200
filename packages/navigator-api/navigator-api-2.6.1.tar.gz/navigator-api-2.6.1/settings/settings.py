# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import sys
from navconfig import config
from navconfig.logging import logging

### Applications (list of applications installed)
APPLICATIONS = [
    'flexroc',
    'dubai'
]

# Debug
DEBUG = config.getboolean('DEBUG', fallback=True)
LOCAL_DEVELOPMENT = (DEBUG is True and sys.argv[0] == 'run.py')
TMP_DIR = config.get('temp_path', section='temp', fallback='/temp')

# upgrade no-files
NOFILES = config.get('ULIMIT_NOFILES', fallback=16384)

"""
Scheduler System
"""
# Schedule System
ENABLE_SCHEDULER = config.getboolean('ENABLE_SCHEDULER', fallback=True)
# Jobs Activation
ENABLE_JOBS = config.getboolean('ENABLE_JOBS', fallback=False)

SCHEDULER_MAX_INSTANCES = config.get('MAX_INSTANCES', fallback=30)
SCHEDULER_GRACE_TIME = config.get('GRACE_TIME', fallback=15)

# PGP Credentials
PGP_KEY_PATH = config.get('pgp_key_path')
PGP_PASSPHRASE = config.get('pgp_passphrase')

# Timezone (For parsedate)
# https://dateparser.readthedocs.io/en/latest/#timezone-and-utc-offset
TIMEZONE = config.get('timezone', section='l18n', fallback='America/New_York')

"""
Databases
"""
# DB Default
# POSTGRESQL Default
DBHOST = config.get('DBHOST', fallback='localhost')
DBUSER = config.get('DBUSER')
DBPWD = config.get('DBPWD')
DBNAME = config.get('DBNAME', fallback='navigator')
DBPORT = config.get('DBPORT', fallback=5432)
if not DBUSER:
    raise Exception('Missing PostgreSQL Default Settings.')

# RETHINKDB
rt_driver = config.get('RT_DRIVER', fallback='rethink')
rt_host = config.get('RT_HOST', fallback='localhost')
rt_port = config.get('RT_PORT', fallback=28015)
rt_database = config.get('RT_DATABASE', fallback='navigator')
rt_user = config.get('RT_USER')
rt_password = config.get('RT_PWD')
rt_database = config.get('RT_DATABASE')


# POSTGRESQL
PG_DRIVER = config.get('PG_DRIVER', fallback='pg')
PG_HOST = config.get('PG_HOST', fallback='localhost')
PG_USER = config.get('PG_USER')
PG_PWD = config.get('PG_PWD')
PG_DATABASE = config.get('PG_DATABASE', fallback='navigator')
PG_PORT = config.get('PG_PORT', fallback=5432)
if not PG_USER:
    raise Exception('Missing PostgreSQL Settings.')


# Postgres Parameters:
POSTGRES_TIMEOUT = config.get('POSTGRES_TIMEOUT', fallback=3600000)
POSTGRES_MIN_CONNECTIONS = config.getint(
    'POSTGRES_MIN_CONNECTIONS', fallback=2)
POSTGRES_MAX_CONNECTIONS = config.getint(
    'POSTGRES_MAX_CONNECTIONS', fallback=200)


database_url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
    user=PG_USER,
    password=PG_PWD,
    host=PG_HOST,
    port=PG_PORT,
    db=PG_DATABASE
)
SQLALCHEMY_DATABASE_URI = database_url

# database for changes (admin)
asyncpg_url = 'postgres://{user}:{password}@{host}:{port}/{db}'.format(
    user=DBUSER,
    password=DBPWD,
    host=DBHOST,
    port=DBPORT,
    db=DBNAME
)

### DWH Connectors
DWH_USER = config.get('DWHUSER', fallback=DBUSER)
DWH_HOST = config.get('DWHHOST', fallback=DBHOST)
DWH_PWD = config.get('DWHPWD', fallback=DBPWD)
DWH_DATABASE = config.get('DWHNAME', fallback=DBNAME)
DWH_PORT = config.get('DWHPORT', fallback=DBPORT)

# read-only access to pg
dwh_url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
    user=PG_USER,
    password=PG_PWD,
    host=PG_HOST,
    port=PG_PORT,
    db=PG_DATABASE
)
# admin: write-access permission over pg
adwh_url = 'postgres://{user}:{password}@{host}:{port}/{db}'.format(
    user=DWH_USER,
    password=DWH_PWD,
    host=DWH_HOST,
    port=DWH_PORT,
    db=DWH_DATABASE
)

## MS SQL Server:
MSSQL_DRIVER = config.get('MSSQL_DRIVER', fallback='sqlserver')
MSSQL_HOST = config.get('MSSQL_HOST', fallback='localhost')
MSSQL_PORT = config.get('MSSQL_PORT', fallback='1433')
MSSQL_USER = config.get('MSSQL_USER')
MSSQL_PWD = config.get('MSSQL_PWD')
MSSQL_DATABASE = config.get('MSSQL_DATABASE')
if not MSSQL_USER:
    raise Exception('Missing Microsoft SQL Server Settings.')

## CASSANDRA
CASSANDRA_DRIVER = config.get('CASSANDRA_DRIVER', fallback='cassandra')
CASSANDRA_HOST = config.get('CASSANDRA_HOST', fallback='127.0.0.1')
CASSANDRA_PORT = config.get('CASSANDRA_PORT', fallback='9042')
CASSANDRA_USER = config.get('CASSANDRA_USER')
CASSANDRA_PWD = config.get('CASSANDRA_PWD')
CASSANDRA_DATABASE = config.get('CASSANDRA_DATABASE')
if not CASSANDRA_USER:
    raise Exception('Missing Cassandra Settings.')

## INFLUXDB
INFLUX_DRIVER = config.get('INFLUX_DRIVER', fallback='cassandra')
INFLUX_HOST = config.get('INFLUX_HOST', fallback='127.0.0.1')
INFLUX_PORT = config.get('INFLUX_PORT', fallback='8086')
INFLUX_USER = config.get('INFLUX_USER')
INFLUX_PWD = config.get('INFLUX_PWD')
INFLUX_DATABASE = config.get('INFLUX_DATABASE')
if not INFLUX_HOST:
    raise Exception('Missing InfluxDB Settings.')

## MYSQL
MYSQL_DRIVER = config.get('MYSQL_DRIVER', fallback='mysql')
MYSQL_HOST = config.get('MYSQL_HOST', fallback='127.0.0.1')
MYSQL_PORT = config.get('MYSQL_PORT', fallback='3306')
MYSQL_USER = config.get('MYSQL_USER')
MYSQL_PWD = config.get('MYSQL_PWD')
MYSQL_DATABASE = config.get('MYSQL_DATABASE')
if not MYSQL_DATABASE:
    raise Exception('Missing mySQL Settings.')

"""
 Paths
"""
API_HOST = config.get('API_HOST')

"""
QuerySet (for QuerySource)
"""

CACHE_HOST = config.get('CACHEHOST', fallback='localhost')
CACHE_PORT = config.get('CACHEPORT', fallback=6379)
CACHE_URL = "redis://{}:{}".format(CACHE_HOST, CACHE_PORT)
REDIS_SESSION_DB = config.get('REDIS_SESSION_DB', fallback=0)

# QuerySet
QUERYSET_DB = config.get('QUERYSET_DB', fallback=0)
QUERYSET_REDIS = CACHE_URL+"/" + str(QUERYSET_DB)

"""
 Memcache
"""
MEMCACHE_HOST = config.get('MEMCACHE_HOST', 'localhost')
MEMCACHE_PORT = config.get('MEMCACHE_PORT', 11211)

"""
 Redash System
"""
REDASH_HOST = 'https://widgets.trocglobal.com'
REDASH_API_KEY = config.get('REDASH_API_KEY')

"""
 Amazon
"""
aws_region = config.get('AWS_REGION', section='AWS', fallback='us-east-1')
aws_bucket = config.get('AWS_BUCKET', section='AWS',
                        fallback='navigator-static-files-2')
aws_key = config.get('AWS_KEY')
aws_secret = config.get('AWS_SECRET')

"""
Amazon AWS Credentials
TODO: iteration over a list of supported s3 buckets
"""
AWS_CREDENTIALS = {
    "default": {
        "use_credentials": True,
        "aws_key": aws_key,
        "aws_secret": aws_secret,
        "region_name": aws_region,
        "bucket_name": aws_bucket
    },
    "navigator": {
        "use_credentials": False,
        "aws_key": aws_key,
        "aws_secret": aws_secret,
        "region_name": aws_region,
        "bucket_name": aws_bucket
    },
    "vision": {
        "use_credentials": False,
        "aws_key": config.get('vision_aws_key'),
        "aws_secret": config.get('vision_aws_secret'),
        "region_name": config.get('vision_aws_region'),
        "bucket_name": config.get('vision_aws_bucket'),
    },
    "viba": {
        "use_credentials": False,
        "aws_key": config.get('viba_aws_key'),
        "aws_secret": config.get('viba_aws_secret'),
        "region_name": config.get('viba_aws_region'),
        "bucket_name": config.get('viba_aws_bucket'),
    }
}

"""
Email Configuration
"""
# email:
EMAIL_USERNAME = config.get('sendgrid_user')
EMAIL_PASSWORD = config.get('sendgrid_password')
EMAIL_PORT = config.get('sendgrid_port', fallback=587)
EMAIL_HOST = config.get('sendgrid_host')

"""
Resource Usage
"""
QUERY_API = config.getboolean('QUERY_API', fallback=True)
SCHEDULER = config.getboolean('SCHEDULER', fallback=True)
SERVICES = config.getboolean('SERVICES', fallback=True)
WEBSOCKETS = config.getboolean('WEBSOCKETS', fallback=True)
API_TIMEOUT = 36000  # 10 minutes
SEMAPHORE_LIMIT = config.getint('SEMAPHORE_LIMIT', fallback=4096)

"""
Notification System
"""
SEND_NOTIFICATIONS = bool(config.get('SEND_NOTIFICATIONS', fallback=True))
TELEGRAM_BOT_TOKEN = config.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = config.get('TELEGRAM_CHAT_ID')

EVENT_CHAT_BOT = config.get('EVENT_CHAT_BOT', fallback=TELEGRAM_BOT_TOKEN)
EVENT_CHAT_ID = config.get('EVENT_CHAT_ID', fallback=TELEGRAM_CHAT_ID)

DEFAULT_RECIPIENT = {
    "name": "Jesus Lara",
    "account": {
        "address": "jesuslarag@gmail.com",
        "phone": "+34692817379"
    }
}

NOTIFY_ON_ERROR = 'dummy'
NOTIFY_ON_SUCCESS = 'dummy'
NOTIFY_ON_FAILURE = 'dummy'
NOTIFY_ON_WARNING = 'dummy'

"""
Authentication and Authorization Backend
"""
ENABLE_AUTH = config.getboolean('ENABLE_AUTH', fallback=True)
# Partner Key (for TrocToken)
PARTNER_KEY = config.get('PARTNER_KEY')
PARTNER_SESSION_TIMEOUT = 200000  # in seconds
CYPHER_TYPE = 'RNC'
AUTH_TOKEN_ISSUER = config.get('AUTH_TOKEN_ISSUER', fallback='Navigator')
AUTH_TOKEN_SECRET = config.get('AUTH_TOKEN_SECRET', fallback=PARTNER_KEY)

AUTH_CREDENTIALS_REQUIRED = config.getboolean(
    'AUTH_CREDENTIALS_REQUIRED', fallback=False
)

AUTH_USER_MODEL = config.get(
    'AUTH_USER_MODEL',
    fallback='navigator.auth.models.User'
)

AUTH_REDIRECT_URI = config.get('AUTH_REDIRECT_URI', fallback='https://nav-api.dev.local:5000/static/welcome.html')
# what happen when a user doesn't exists?
# possible values are: create (user is created), raise (a UserDoesntExists exception raises)
# and ignore, session is created but user is missing.
AUTH_MISSING_ACCOUNT = config.get(
    'AUTH_MISSING_ACCOUNT', fallback='create'
)
# List of function callbacks called (in order) when a user is
AUTH_SUCCESSFUL_CALLBACKS = (
    'resources.auth.last_login',
    'resources.auth.saving_troc_user'
)


AUTHENTICATION_BACKENDS = (
 #'navigator.auth.backends.TrocToken',
 #'navigator.auth.backends.TokenAuth',
 #'navigator.auth.backends.GoogleAuth',
 # 'navigator.auth.backends.OktaAuth',
 #'navigator.auth.backends.ADFSAuth',
 # 'navigator.auth.backends.AzureAuth',
 #'navigator.auth.backends.GithubAuth',
 'navigator_auth.backends.BasicAuth',
 'navigator_auth.backends.DjangoAuth',
 'navigator_auth.backends.NoAuth',
)

SECRET_KEY = 'CAMISA'  # in dev, avoid random secret key

AUTHORIZATION_MIDDLEWARES = (
    # 'navigator.auth.middlewares.django_middleware',
    # 'navigator.auth.middlewares.troctoken_middleware',
)

SESSION_URL = "redis://{}:{}/{}".format(CACHE_HOST,
                                        CACHE_PORT, REDIS_SESSION_DB)
CACHE_PREFIX = config.get('CACHE_PREFIX', fallback='navigator')
SESSION_PREFIX = '{}_session'.format(CACHE_PREFIX)
SESSION_TIMEOUT = config.getint('SESSION_TIMEOUT', fallback=360000)
SESSION_KEY = config.get('SESSION_KEY', fallback='id')
SECRET_KEY = 'CAMISA'  # avoid using fixed secret keys for JWT
SESSION_STORAGE = 'NAVIGATOR_SESSION_STORAGE'
SESSION_OBJECT = 'NAV_SESSION'

# GOOGLE
GOOGLE_CLIENT_ID = config.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = config.get('GOOGLE_CLIENT_SECRET')
GOOGLE_API_SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "email"
]

# Okta
OKTA_CLIENT_ID = config.get('OKTA_CLIENT_ID')
OKTA_CLIENT_SECRET = config.get('OKTA_CLIENT_SECRET')
OKTA_DOMAIN = config.get('OKTA_DOMAIN')
OKTA_APP_NAME = config.get('OKTA_APP_NAME')

# ADFS SSO
ADFS_SERVER = config.get('ADFS_SERVER')
ADFS_CLIENT_ID = config.get('ADFS_CLIENT_ID')
ADFS_RELYING_PARTY_ID = config.get('ADFS_RELYING_PARTY_ID')
ADFS_RESOURCE = config.get('ADFS_RESOURCE')
ADFS_AUDIENCE = config.get('ADFS_AUDIENCE')
ADFS_ISSUER = config.get('ADFS_ISSUER')
ADFS_SCOPES = config.get(
    'ADFS_SCOPES', fallback='https://graph.microsoft.com/.default')
ADFS_TENANT_ID = config.get('ADFS_TENANT_ID', fallback=None)
USERNAME_CLAIM = config.get('USERNAME_CLAIM')
GROUP_CLAIM = config.get('GROUP_CLAIM')
ADFS_LOGIN_REDIRECT_URL = config.get('ADFS_LOGIN_REDIRECT_URL')
ADFS_CALLBACK_REDIRECT_URL = config.get('ADFS_CALLBACK_REDIRECT_URL')



adfs_mapping = {
    "first_name": "given_name",
    "last_name": "family_name",
    "email": "email"
}
AZURE_AD_SERVER = config.get(
    'AZURE_AD_SERVER',
    fallback="login.microsoftonline.com"
)
ADFS_CLAIM_MAPPING = config.get('ADFS_CLAIM_MAPPING', fallback=adfs_mapping)

# Microsoft Azure
AZURE_ADFS_CLIENT_ID = config.get('AZURE_ADFS_CLIENT_ID')
AZURE_ADFS_CLIENT_SECRET = config.get('AZURE_ADFS_CLIENT_SECRET')
AZURE_ADFS_TENANT_ID = config.get('AZURE_ADFS_TENANT_ID', fallback='common')
AZURE_ADFS_SECRET = config.get('AZURE_ADFS_SECRET')
AZURE_ADFS_DOMAIN = config.get(
    'AZURE_ADFS_DOMAIN', fallback='contoso.onmicrosoft.com')

default_scopes = "User.Read,User.Read.All,User.ReadBasic.All,openid"
AZURE_ADFS_SCOPES = [
    e.strip()
    for e in list(config.get("AZURE_ADFS_SCOPES", fallback="").split(","))
]

## Github Support:
GITHUB_CLIENT_ID = config.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = config.get('GITHUB_CLIENT_SECRET')


DJANGO_SESSION_DB = config.get('DJANGO_SESSION_DB', fallback=REDIS_SESSION_DB)
DJANGO_SESSION_URL = f"redis://{CACHE_HOST}:{CACHE_PORT}/{DJANGO_SESSION_DB}"
DJANGO_SESSION_PREFIX = config.get('DJANGO_SESSION_PREFIX', fallback=f'{CACHE_PREFIX}_session')
DJANGO_USER_MAPPING = {
    "groups": "groups",
    "programs": "programs",
    "modules": "modules",
    "api_url": "api_url",
    "api_query": "api_query",
    "filtering_fixed": "filtering_fixed",
    "hierarchy": "hierarchy",
    "employee": "employee"
}

### QuerySource variables and Extensions
# Variables: replacement on field values.
QUERYSOURCE_VARIABLES = {
    "current_seasonality": "resources.functions.current_seasonality",
    "first_day": "querysource.libs.functions.first_day",
    "last_day": "querysource.libs.functions.last_day",
}

# FILTERS: functions called on "filter" process.
QUERYSOURCE_FILTERS = {
    "qry_options": "querysource.libs.functions.query_options",
    "grouping_set": "querysource.libs.functions.grouping_set",
    "group_by_child": "querysource.libs.functions.group_by_child",
}
