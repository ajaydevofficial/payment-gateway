from django.db import models

# Create your models here.
class order_id(models.Model):
    name = models.CharField(default='',max_length=200)
    id = models.IntegerField(default=1759,primary_key=True)

    def __str__(self):
        return str(self.name)
