from django.contrib import admin

# Register your models here.

from .models import CryptoCoin


admin.site.register(CryptoCoin)
