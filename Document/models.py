from django.db import models

# Create your models here.
class document(models.Model):
    name = models.CharField(max_length=200)
    doc = models.FileField()

    def __init__(self):
        return self.name
