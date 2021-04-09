# we want to load Celery automatically when the django starts
from .celery import app as celery_app

# list of names of our apps
__all__ = ['celery_app']