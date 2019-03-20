from django.db import models

# Create your models here.
class order_success(models.Model):
    
    order_id = models.CharField(max_length = 200)
    order_amount = models.CharField(max_length = 200)
    txn_id = models.CharField(max_length = 200)
    txn_amount = models.CharField(max_length = 200)
    txn_date = models.CharField(max_length = 200)
    currency = models.CharField(max_length = 200)
    status = models.CharField(max_length = 200)
    resp_msg = models.CharField(max_length = 1000)
    payment_mode = models.CharField(max_length = 200)
    gateway_name = models.CharField(max_length = 200)
    bank_txn_id = models.CharField(max_length = 200)
    bank_name = models.CharField(max_length = 200)

    def __str__(self):
        return str(order_id)
