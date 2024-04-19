# Praetorian API

Hi. I'm praetorian Cornelius ⚔️. My main task is to protect the Roman emperors 🤴, but in my free time I also like to protect
software companies with my shield 🛡.

---

Praetorian is an information security system providing protection across all major areas of software companies.

Important aspects of the system: ...

## Installation

We use [poetry](https://python-poetry.org/) to manage our dependencies. Use `poetry install` to create new environment
and install all required dependencies.

## Database load

1. Run command for making roles : `python manage.py sync_roles`
2. Seed fixtures to the database: `python manage.py loaddata api_keys languages users devices remotes services projects users_projects_devices`
3. Run command for making permissions: `python manage.py sync_perms`

## Database dump

- Loading specific database table content into json:

> `python manage.py dumpdata core.ApiKey > apps/core/fixtures/api_keys.json`

## Authentication

1. LDAP: `apps.api.auth.ldap_backend.LDAPBackend`
2. TOKEN: `apps.api.auth.token_backend.TokenBackend`

### LDAP Content setup
```json
{
  "BIND_DN": "",
  "BASE_URL": "",
  "GROUP_TYPE": "GroupOfNamesType",
  "SERVER_URI": "",
  "USER_SEARCH": {
    "scope": 2,
    "base_dn": "",
    "filterstr": "mail=%(user)s"
  },
  "GROUP_SEARCH": {
    "scope": 2,
    "base_dn": "",
    "filterstr": "(objectClass=group)"
  },
  "BIND_PASSWORD": "",
  "USER_ATTR_MAP": {
    "name": "givenName",
    "email": "mail",
    "phone": "telephoneNumber",
    "surname": "sn",
    "username": "sAMAccountName",
    "is_active": "enabled"
  },
  "USER_LOGIN_ATTR": "userPrincipalName",
  "AUTH_SOURCE_LDAP_NAME": ""
}
```

## Docker

```bash
docker network ls
docker network inspect praetorian
```
ping db
```bash
docker-compose exec web python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('db', 5432)); print('Successfully connected'); s.close()"
```
open container using bash
```bash
docker-compose exec <container_name> bash
```

start python shell in container
```bash
docker-compose exec web python manage.py shell
```
then use python
```python
from apps.core.models import User
print(User.objects.all())
```

---
Developed with 💙 and ☕️ by [Adam Žúrek](https://zurek11.github.io/), Erik Belák
with the support of [BACKBONE s.r.o.](https://www.backbone.sk/), 2024 (C)
