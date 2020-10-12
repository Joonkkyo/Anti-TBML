import django_tables2 as tables
from .models import SanctionList


class SanctionTable(tables.Table):
    class Meta:
        model = SanctionList
    # queryset = SanctionList.objects.all()
    # template_name = 'django_tables2/bootstrap.html'