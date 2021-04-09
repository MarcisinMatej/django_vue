from django.urls import path

from emc_project.consumers import CryptoCoinConsumer

ws_urlpatterns = [
    path('ws/coins/', CryptoCoinConsumer.as_asgi())
]