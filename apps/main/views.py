from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

import json
import math
import random


@csrf_exempt
def get_near_shops(request):
    # {lat: , long: }

    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')

            print(data)

            if(data == ''):
                return HttpResponse(status=400)
            data = json.loads(data)

            if not data['lat'] or not data['long']:
                return HttpResponse(status=400)

        except Exception as e:
            print(e)

        shops = Shop.objects.all()

        dist = 0.5

        # 1 градус широты = 111 км
        long1 = data['long'] - dist / \
            abs(math.cos(math.radians(data['lat'])) * 111.0)
        long2 = data['long'] + dist / \
            abs(math.cos(math.radians(data['lat'])) * 111.0)
        lat1 = data['lat'] - (dist / 111.0)
        lat2 = data['lat'] + (dist / 111.0)

        shops = Shop.objects.filter(location__lat__range=(lat1, lat2)).filter(
            location__long__range=(long1, long2))
        result = []
        for shop in shops:

            avalible_promocodes = shop.promocode_templates.all()

            random_promo = avalible_promocodes[random.randint(
                0, len(avalible_promocodes) - 1)]

            result.append({
                'id': shop.id,
                'name': shop.name,
                'location': {
                    'lat': shop.location.lat,
                    'long': shop.location.long
                },
                'promocode': {
                    'id': random_promo.id,
                    'text': random_promo.text
                }
            })

        # print(result)
        return HttpResponse(json.dumps(result), status=200)

    else:
        return HttpResponse(status=405)
