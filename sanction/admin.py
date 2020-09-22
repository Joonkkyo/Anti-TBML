from django.contrib import admin
from sanction.models import SanctionList


@admin.register(SanctionList)
class SanctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'program')
# Register your models here.
