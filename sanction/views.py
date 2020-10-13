from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig, SingleTableView
from sanction.models import SanctionList
import django_tables2 as tables
from .tables import SanctionTable
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView


class TableView(tables.SingleTableView):
    table_class = SanctionTable
    paginate_by = 10
    paginate_orphans = 5
    queryset = SanctionList.objects.all()
    template_name = 'django_tables2/bootstrap.html'

# class SanctionLV(SingleTableView):
#     # 모델의 인스턴스 데이터 객체로 변환
#     # table = SanctionTable(SanctionList.objects.all())
#     # RequestConfig(request).configure(table)
#     # content = {'table': table}
#     model = SanctionList
#     table_class = SanctionTable
#     template_name = 'sanction/sanction_list.html'
#     table_pagination = False

# class SanctionLV(ListView):
#     model = SanctionList
#     paginate_by = 10
#     paginate_orphans = 5
#     template_name = 'sanction/sanction_list.html'
# Create your views here.
