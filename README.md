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

---
Developed with 💙 and ☕️ by [Adam Žúrek](https://zurek11.github.io/), Erik Belák
with the support of [BACKBONE s.r.o.](https://www.backbone.sk/), 2023 (C)
