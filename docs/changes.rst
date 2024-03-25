Changelog
=========


0.2 (rolling release)
---------------------

- Fix pylint-reports and optimize pylint-config.

- Migrate from drf_yasg2 back to drf_yasg.
  drf_yasg2 was fork of the umaintained drf_yasg.

- Upgrade django to latest 4.2.11.
  see https://github.com/ScoutsGidsenVL/werkwinkeldatabank-backend/pull/29

- Fix alerts about information exposure through an exception
  see https://github.com/ScoutsGidsenVL/werkwinkeldatabank-backend/security/code-scanning/1
  see https://github.com/ScoutsGidsenVL/werkwinkeldatabank-backend/security/code-scanning/2

- Add justfile as modern alternative to a makefile.
  See https://just.systems/man

- Add codesql-scanning
  see https://github.com/ScoutsGidsenVL/werkwinkeldatabank-backend/pull/5

- Take over maintenance of the project by Wouter Vanden Hove <wouter@libranet.eu>.

0.1 (Pre 2023)
--------------

- Django project created by Inuits.