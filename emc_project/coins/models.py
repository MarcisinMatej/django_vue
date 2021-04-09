"""
Django models, note that after defining new class/model you must run migrations so Django can find the new model.
For migrations run
    manage.py makemigrations
    manage.py migrate
"""

from django.db import models

# Create your models here.
# we need class for coins, store coin value before and after update
class CryptoCoin(models.Model):
    # todo move this to init, I do not think, that it should be in the class params
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    price = models.FloatField(default=0, blank=True)
    rank = models.IntegerField(default=0, blank=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    # define so the class can be automatically ordered
    class Meta:
        ordering = ['rank']