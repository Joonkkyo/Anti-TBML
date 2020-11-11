from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='documents/')
    file_path = models.FileField(upload_to='documents/', null=True)
