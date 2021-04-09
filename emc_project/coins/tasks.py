"""
Definitions of tasks for the celery app
"""
from asgiref.sync import async_to_sync
import requests
from django.forms.models import model_to_dict
from celery import shared_task
from channels.layers import get_channel_layer
from .models import CryptoCoin

# async function
channel_layer = get_channel_layer()

@shared_task()
def get_coins_data():
    """
    Get top 100 listings of crypto coins from the congeck.com
    Coingecko api request to get first 100 listing is documented here: https://www.coingecko.com/en/api
    The URL was coppied from the section get coins markets
    :return:
    """
    get_market_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    # rewuest returns response object, which we serialize to json, so we can pass it to index
    data = requests.get(get_market_url).json()
    coins = []
    # iterate over all coins in the response to:
    #   1. store/update data in our database
    #   2. create list of coin object to be sent to FE
    for crypt_coin in data:
        # we use ticker symbol as UID in the database
        # created is flag if the coin object was created or not (if not, it was just loade from DB)
        obj, created = CryptoCoin.objects.get_or_create(symbol=crypt_coin['symbol'])

        # TODO replace this into the init methd
        # fill the object with data
        obj.name = crypt_coin['name']
        obj.symbol = crypt_coin['symbol']
        # check the change of price compared to previous value
        if obj.price > crypt_coin['current_price']:
            state = 'fall'
        elif obj.price < crypt_coin['current_price']:
            state = 'raise'
        else:
            state = 'same'

        obj.price = crypt_coin['current_price']
        obj.rank = crypt_coin['market_cap_rank']
        obj.image = crypt_coin['image']

        # save the object into the DB
        obj.save()

        # convert our object to dict, so we can send it to FE as dictionary and add state key-value
        new_data_dict = model_to_dict(obj)
        # add state
        new_data_dict.update({'state':state})
        coins.append(new_data_dict)

    # we need to call channels consumer
    async_to_sync(channel_layer.group_send)('crypto_coins_group', {'type': 'send_new_data', 'text': coins})