from .base import *

DEBUG = True

TIME_ZONE = 'Europe/Bratislava'

MIDDLEWARE += [
    'apps.api.middleware.signature.SignatureMiddleware'
]

# Emails
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = f'{BASE_DIR}/tmp/emails'

EMAIL_BACKEND = 'django_imap_backend.ImapBackend'

EMAIL_IMAP_SECRETS = [
    {
        'HOST': 'imap.backbone.sk',
        'USER': 'testing@backbone.sk',
        'PASSWORD': 'smecarovni123.',
        'MAILBOX': 'praetorian',
        'SSL': False
    }
]
