from django.db import models

# Create your models here.
class RootTable (models.Model):
    abc = models.CharField(max_length=200)
