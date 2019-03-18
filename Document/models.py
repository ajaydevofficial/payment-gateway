from django.db import models

# Create your models here.
class document(models.Model):
    name = models.CharField(max_length=200)
    doc = models.FileField()

    def __str__(self):
        return str(self.name)
