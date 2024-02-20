# Generated by Django 3.2.15 on 2024-02-13 11:48

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0037_auto_20210125_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('customer_surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес доставки')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]