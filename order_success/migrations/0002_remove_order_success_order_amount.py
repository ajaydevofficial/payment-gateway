# Generated by Django 2.1.7 on 2019-03-20 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_success', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_success',
            name='order_amount',
        ),
    ]
