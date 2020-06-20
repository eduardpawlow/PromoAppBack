from django.contrib import admin
from .models import *


class MapMarkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'lat', 'long')

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'full_location')

    def full_location(self, obj):
        return 'Lat: %f, Long: %f' % (obj.location.lat, obj.location.long)
    full_location.short_description = 'Локация'

# class PromocodeTemplateAdmin(admin.ModelAdmin):
#     list_display = ('id', 'lat', 'long')

class ActivePromocodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'end_date', 'code')

class VkUserAdmin(admin.ModelAdmin):
    list_display = ('vk_id',)


admin.site.register(MapMarker, MapMarkerAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(PromocodeTemplate)
admin.site.register(ActivePromocode, ActivePromocodeAdmin)
admin.site.register(VkUser, VkUserAdmin)