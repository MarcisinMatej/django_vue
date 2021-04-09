import os

from celery import Celery

# tell the os where are the sttings and modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emc_project.settings')

app = Celery('emc_project')
# we use CELERY prefix for celery object in the settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# configure scheaduler -> how often the tasks should be executed
app.conf.beat_schedule = {
    'get_coins_data_30s': {
        # path to function
        'task': 'coins.tasks.get_coins_data',
        'schedule': 10.0
    }
}

app.autodiscover_tasks()