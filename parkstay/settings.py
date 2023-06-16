import os
import confy
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
confy.read_environment_file(BASE_DIR+"/.env")
os.environ.setdefault("BASE_DIR", BASE_DIR)
from ledger.settings_base import *

ROOT_URLCONF = 'parkstay.urls'
SITE_ID = 1
#DATABASES['site_queue_manager'] = {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR+'/parkstay/cache/site_manager_db.sqlite3',
#    } 
#DATABASE_ROUTERS.append('django_site_queue.models.SiteQueueManagerDBRouter')
#DATABASE_APPS_MAPPING['site_queue_manager'] = 'site_queue_manager'

# number of seconds before expiring a temporary booking
BOOKING_TIMEOUT = 600

INSTALLED_APPS += [
    'bootstrap3',
    'parkstay',
    'taggit',
    'rest_framework',
    'rest_framework_gis',
#    'django_site_queue',
]

MIDDLEWARE_CLASSES += [
    'parkstay.middleware.BookingTimerMiddleware'
]

# maximum number of days allowed for a booking
PS_MAX_BOOKING_LENGTH = 28 

# minimum number of remaining campsites to trigger an availaiblity warning
PS_CAMPSITE_COUNT_WARNING = 10

# number of days before clearing un unpaid booking
PS_UNPAID_BOOKING_LAPSE_DAYS = 5

WSGI_APPLICATION = 'parkstay.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'parkstay.perms.OfficerPermission',
    )
}

# disable Django REST Framework UI on prod
if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']=('rest_framework.renderers.JSONRenderer',)
else:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']=('rest_framework.renderers.JSONRenderer','rest_framework_csv.renderers.CSVRenderer')


TEMPLATES[0]['DIRS'].append(os.path.join(BASE_DIR, 'parkstay', 'templates'))
TEMPLATES[0]['DIRS'].append(os.path.join(BASE_DIR, 'django_site_queue', 'templates'))
TEMPLATES[0]['OPTIONS']['context_processors'].append('parkstay.context_processors.parkstay_url')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'parkstay', 'cache'),
    }
}
STATICFILES_DIRS.append(os.path.join(os.path.join(BASE_DIR, 'parkstay', 'static')))


BPAY_ALLOWED = env('BPAY_ALLOWED',False)

OSCAR_BASKET_COOKIE_OPEN = 'parkstay_basket'


CRON_CLASSES = [
    #'parkstay.cron.SendBookingsConfirmationCronJob',
    'parkstay.cron.UnpaidBookingsReportCronJob',
    #'parkstay.cron.OracleIntegrationCronJob', # Disabled on the 16/06/2023 by PVS
]

# Additional logging for parkstay
LOGGING['loggers']['booking_checkout'] = {
    'handlers': ['console'],
    'level': 'INFO'
}
os.environ['LEDGER_REFUND_TRANSACTION_CALLBACK_MODULE'] = 'parkstay:parkstay.api.refund_transaction_callback'
os.environ['LEDGER_INVOICE_TRANSACTION_CALLBACK_MODULE'] = 'parkstay:parkstay.api.invoice_callback'


SYSTEM_NAME = env('SYSTEM_NAME', 'Parkstay WA')
EMAIL_FROM = env('EMAIL_FROM', ADMINS[0])
DEFAULT_FROM_EMAIL = EMAIL_FROM
WAITING_QUEUE_ENABLED = env('WAITING_QUEUE_ENABLED',"False")
PS_PAYMENT_SYSTEM_ID = env('PS_PAYMENT_SYSTEM_ID', 'S019')
if not VALID_SYSTEMS:
    VALID_SYSTEMS = [PS_PAYMENT_SYSTEM_ID]
EXPLORE_PARKS_URL = env('EXPLORE_PARKS_URL', 'https://parks.dpaw.wa.gov.au/park-stay')
PARKS_EXTERNAL_BOOKING_URL =env('PARKS_EXTERNAL_BOOKING_URL','https://parkstaybookings.dbca.wa.gov.au')
PARKSTAY_EXTERNAL_URL = env('PARKSTAY_EXTERNAL_URL','https://parkstay.dbca.wa.gov.au')
DEV_STATIC = env('DEV_STATIC',False)
DEV_STATIC_URL = env('DEV_STATIC_URL')
DEPT_DOMAINS = env('DEPT_DOMAINS', ['dpaw.wa.gov.au', 'dbca.wa.gov.au'])
#LEDGER_REFUND_EMAIL = env('LEDGER_REFUND_EMAIL', False )
os.environ['LEDGER_REFUND_EMAIL'] = 'True'
VERSION_NO = '3.12'
# Only change if you make changes to Booking Properties
BOOKING_PROPERTY_CACHE_VERSION='v1.03'
QUEUE_DOMAIN = env('QUEUE_DOMAIN','')
QUEUE_URL = env('QUEUE_URL','')
QUEUE_ACTIVE_HOSTS = env('QUEUE_ACTIVE_HOSTS','')
CAMPSITE_BOOKING_API_KEY = env('CAMPSITE_BOOKING_API_KEY','')

# Use git commit hash for purging cache in browser for deployment changes
GIT_COMMIT_HASH = ''
GIT_COMMIT_DATE = ''
if  os.path.isdir(BASE_DIR+'/.git/') is True:
    GIT_COMMIT_DATE = os.popen('cd '+BASE_DIR+' ; git log -1 --format=%cd').read()
    GIT_COMMIT_HASH = os.popen('cd  '+BASE_DIR+' ; git log -1 --format=%H').read()
if len(GIT_COMMIT_HASH) == 0:
    GIT_COMMIT_HASH = os.popen('cat /app/git_hash').read()
    if len(GIT_COMMIT_HASH) == 0:
       print ("ERROR: No git hash provided")

