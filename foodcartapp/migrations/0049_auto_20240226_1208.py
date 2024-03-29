# Generated by Django 3.2.15 on 2024-02-26 08:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20240226_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='дата обзванивания'),
        ),
    ]
