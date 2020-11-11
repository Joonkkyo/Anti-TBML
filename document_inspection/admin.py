from django.contrib import admin
from document_inspection.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'picture', 'file_path')
