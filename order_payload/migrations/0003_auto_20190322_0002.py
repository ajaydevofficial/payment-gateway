# Generated by Django 2.1.7 on 2019-03-21 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_payload', '0002_order_id_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_id',
            name='order_id',
        ),
        migrations.AlterField(
            model_name='order_id',
            name='id',
            field=models.IntegerField(default=1759, primary_key=True, serialize=False),
        ),
    ]