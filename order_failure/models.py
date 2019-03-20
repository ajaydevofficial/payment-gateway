from django.db import models

# Create your models here.
class order_failure(models.Model):

    order_id = models.CharField(max_length = 200,default='')
    txn_id = models.CharField(max_length = 200,default='')
    txn_amount = models.CharField(max_length = 200,default='')
    txn_date = models.CharField(max_length = 200,default='')
    currency = models.CharField(max_length = 200,default='')
    status = models.CharField(max_length = 200,default='')
    resp_msg = models.CharField(max_length = 1000,default='')
    payment_mode = models.CharField(max_length = 200,default='')
    gateway_name = models.CharField(max_length = 200,default='')
    bank_txn_id = models.CharField(max_length = 200,default='')
    bank_name = models.CharField(max_length = 200,default='')

    def __str__(self):
        return self.order_id
