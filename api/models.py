from django.db import models

# Create your models here.
class FilterImg(models.Model):
    image = models.ImageField(upload_to="images/")