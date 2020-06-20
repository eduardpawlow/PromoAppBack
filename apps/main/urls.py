from django.urls import path
from .views import *

urlpatterns = [
    path('getshops/', get_near_shops, name="getshop"),
    path('createpromocode/', createpromocode, name="createpromocode"),
    path('getallpromocodes/<int:vk_id>/',
         getallpromocodes, name="getallpromocodes"),
]
