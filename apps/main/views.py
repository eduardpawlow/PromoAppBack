from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

from uuid import uuid4
import json
import math
import random
import datetime


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

        dist = 0.2

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

            if len(avalible_promocodes) != 0:
                random_promo = avalible_promocodes[random.randint(
                    0, len(avalible_promocodes) - 1)]

            else:
                continue

            result.append({
                'id': shop.id,
                'name': shop.name,
                'location': {
                    'lat': shop.location.lat,
                    'long': shop.location.long
                },
                'promocode': {
                    'id': random_promo.id,
                    'text': random_promo.text,
                    'img': random_promo.image.url if random_promo.image != None else None
                }
            })

        # print(result)
        return HttpResponse(json.dumps(result), status=200)

    else:
        return HttpResponse(status=405)


@csrf_exempt
def createpromocode(request):
    # {vk_id, promocode_id, }

    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')

            print(data)

            if(data == ''):
                return HttpResponse(status=400)
            data = json.loads(data)

            if not data['vk_id'] or not data['promocode_id']:
                return HttpResponse(status=400)

        except Exception as e:
            print(e)

        try:
            [vk_user, is_created] = VkUser.objects.get_or_create(
                vk_id=int(data['vk_id']))
            promoTemp = PromocodeTemplate.objects.get(id=data['promocode_id'])

            print(vk_user)

            life_period = datetime.timedelta(minutes=15)
            end_date = datetime.datetime.now() + life_period

            code = uuid4().hex.upper()[:10]

            createdPromocode = ActivePromocode(
                text=promoTemp,
                vk_user=vk_user,
                end_date=end_date,
                code=code
            )

            createdPromocode.save()

            # result = {
            #     'text': createdPromocode.text.text,
            #     'shop': createdPromocode.text.shop.name,
            #     'end_date': createdPromocode.end_date.strftime("%d.%m.%y %I:%M"),
            #     'vk_user': vk_user.id,
            #     'code': code
            # }

        except Exception as e:
            print(e)
            return HttpResponse(status=400)

        return HttpResponse(json.dumps({'status': True}), status=200)

    else:
        return HttpResponse(status=405)


@csrf_exempt
def getallpromocodes(request, vk_id):
    allPromocodes = ActivePromocode.objects.filter(vk_user__vk_id=400)
    result = []

    for val in allPromocodes:
        result.append({
            'text': val.text.text,
            'shop': val.text.shop.name,
            'end_date': val.end_date.strftime("%d.%m.%y %I:%M"),
            'vk_user': val.vk_user.id,
            'code': val.code
        })

    return HttpResponse(json.dumps(result), status=200)
