from django.db import models
from uuid import uuid4


class VkUser(models.Model):
    vk_id = models.IntegerField(
        verbose_name='VK ID'
    )

    class Meta:
        pass


class MapMarker(models.Model):

    lat = models.FloatField(verbose_name="Широта")

    long = models.FloatField(verbose_name="Долгота")

    class Meta:
        pass


class Shop(models.Model):
    name = models.TextField(
        verbose_name="Название магазина"
    )

    location = models.ForeignKey(to="MapMarker", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        pass


class PromocodeTemplate(models.Model):
    text = models.TextField(
        verbose_name="Текст промокода",
        max_length=400
    )

    def custom_path(self, filename):
        path = 'images/promocodes/'

        ext = filename.split('.')[-1]
        return '%s%s.%s' % (path, uuid4().hex, ext)

    image = models.ImageField(
        upload_to=custom_path,
        verbose_name='Изображение',
        blank=True,
        null=True
    )

    shop = models.ForeignKey(
        to="Shop",
        related_name="promocode_templates",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.text

    class Meta:
        pass


class ActivePromocode(models.Model):
    text = models.ForeignKey(
        to=PromocodeTemplate,
        on_delete=models.CASCADE,
        related_name='active_promocode'
    )

    vk_user = models.ForeignKey(
        to="VkUser",
        on_delete=models.DO_NOTHING,
        related_name='active_promocodes',
        blank=True,
        null=True
    )

    end_date = models.DateTimeField(
        verbose_name="Закончится в",
    )

    code = models.TextField(
        verbose_name="Промокод",
        max_length=20
    )

    class Meta:
        pass
