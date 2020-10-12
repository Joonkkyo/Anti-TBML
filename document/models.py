from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Document(models.Model):
    document = models.ImageField(upload_to='documents/%Y/%m/%d', default='documents/no_image.png')

    upload_time = models.DateTimeField(auto_now_add=True)