from django.db import models

class File(models.Model):
    name = models.CharField(max_length=500)
    file_path = models.FileField(upload_to='documents/', null=True, verbose_name="파일 경로")

    def __str__(self):
        return self.name+":"+str(self.file_path)