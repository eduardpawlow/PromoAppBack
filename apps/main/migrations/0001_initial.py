# Generated by Django 3.0.3 on 2020-06-20 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapMarker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('long', models.FloatField(verbose_name='Долгота')),
            ],
        ),
        migrations.CreateModel(
            name='VkUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vk_id', models.IntegerField(verbose_name='VK ID')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название магазина')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.MapMarker')),
            ],
        ),
        migrations.CreateModel(
            name='PromocodeTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=400, verbose_name='Текст промокода')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='promocode_templates', to='main.Shop')),
            ],
        ),
        migrations.CreateModel(
            name='ActivePromocode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateTimeField(verbose_name='Закончится в')),
                ('code', models.TextField(max_length=20, verbose_name='Промокод')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='active_promocode', to='main.Shop')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active_promocode', to='main.PromocodeTemplate')),
            ],
        ),
    ]