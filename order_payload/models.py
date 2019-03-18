from django.db import models

# Create your models here.
class order_id(models.Model):
    order_id = models.IntegerField(default=1759)

    def __str__(self):
        return 'ORDER_ID'
