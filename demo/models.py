from django.db import models

# Create your models here.
class Demo(models.Model):
    name = models.TextField()
    age = models.TextField()

    class Meta:
        db_table = 'demo'