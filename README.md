# Praetorian API

Hi. I'm a praetorian ⚔️. My main task is to protect the Roman emperors 🤴, but in my free time I also like to protect
software companies with my shield 🛡.

---

Praetorian is an information security system providing protection across all major areas of software companies.

Important aspects of the system: ...

## Installation

We use [poetry](https://python-poetry.org/) to manage our dependencies. Use `poetry install` to create new environment
and install all required dependencies.

## Database dump and load

- Loading specific database table content into json:

> `python manage.py dumpdata core.ApiKey > apps/core/fixtures/api_keys.json`

- Seed multiple fixtures to the database:

> `python manage.py loaddata api_keys languages users devices services remotes projects`

---
Developed with 💙 and ☕️ by [Adam Žúrek](https://zurek11.github.io/)
with the support of [BACKBONE s.r.o.](https://www.backbone.sk/), 2020 (C)
