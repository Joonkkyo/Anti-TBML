from django.contrib import admin
from document_inspection.models import File

@admin.register(File)
class SanctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_path')