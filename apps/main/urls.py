from django.urls import path
from .views import *

urlpatterns = [
    path('getshops/', get_near_shops, name="getshop"),
]
