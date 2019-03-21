# Generated by Django 2.1.7 on 2019-03-21 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='order_refund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='', max_length=200)),
                ('txn_id', models.CharField(default='', max_length=200)),
                ('txn_amount', models.CharField(default='', max_length=200)),
                ('txn_date', models.CharField(default='', max_length=200)),
                ('currency', models.CharField(default='', max_length=200)),
                ('status', models.CharField(default='', max_length=200)),
                ('resp_msg', models.CharField(default='', max_length=1000)),
                ('payment_mode', models.CharField(default='', max_length=200)),
                ('gateway_name', models.CharField(default='', max_length=200)),
                ('bank_txn_id', models.CharField(default='', max_length=200)),
                ('bank_name', models.CharField(default='', max_length=200)),
                ('refund_amount', models.CharField(default='', max_length=200)),
            ],
        ),
    ]