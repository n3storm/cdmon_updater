CDMON dynamic domain services updater
=====================================

CDMON dynamic domain service updater using urllib2 and BeautifulSoup and Logging.

The goal is to have a robust updater to rely:
- Can use several "whatismyip" providers as failback.
- Logs errors

INSTALL
=======

Clone this project and run "python setup.py install" as a user with privileges.

TODO
====

- Mail on errors
- Use a config file /etc/cdmon_updater.ini
