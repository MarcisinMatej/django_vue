# Django-vue Equity-market-cap project
Simple Django app with Vue front-end which will reguralry query API to get latest values for different equities.

The app is using redis, Celery for mesage management.
For the ease of development we use VUE with CDN instead of full installation. 


# Installation


## Runnig app in dev mode
Note, this app was developed on windows, however the command should be same for unix-based platforms.


```bash
# move to project directory
cd emc_project
# colect static files
manage.py colect static
# start local server
manage.py runserver
```

