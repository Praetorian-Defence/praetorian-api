from .base import *

DEBUG = True

TIME_ZONE = 'Europe/Bratislava'

MIDDLEWARE += [
    'apps.api.middleware.signature.SignatureMiddleware'
]

EMAIL_BACKEND = 'django_imap_backend.ImapBackend'

EMAIL_IMAP_SECRETS = [
    {
        'HOST': os.getenv('EMAIL_HOST', None),
        'USER': os.getenv('EMAIL_HOST_USER', None),
        'PASSWORD': os.getenv('EMAIL_HOST_PASSWORD', None),
        'MAILBOX': os.getenv('EMAIL_IMAP_MAILBOX', 'praetorian'),
        'SSL': False
    }
]
