from django.db import models

# Create your models here.
class order_id(models.Model):
    order_id = models.IntegerField(max_digits=100)

    def __str__(self):
        return 'ORDER_ID'
