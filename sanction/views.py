from django.views.generic import ListView
from .models import SanctionList
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView


class SanctionLV(ListView):
    model = SanctionList
    template_name = "sanction/sanction_list.html"
    context_object_name = "sanctions"

    def get_queryset(self):
        sanction_all = SanctionList.objects.all()
        page = int(self.request.GET.get('p', 1))
        paginator = Paginator(sanction_all, 10)
        queryset = paginator.get_page(page)
        return queryset

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
