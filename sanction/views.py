from django.views.generic import ListView
from .models import SanctionList
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView


# class SanctionLV(ListView):
#     model = SanctionList
#     template_name = "sanction/sanction_list.html"
#     context_object_name = "sanctions"
#
#     def get_queryset(self):
#         sanction_all = SanctionList.objects.all()
#         page = int(self.request.GET.get('p', 1))
#         paginator = Paginator(sanction_all, 10)
#         queryset = paginator.get_page(page)
#         return queryset


def sanction_list(request):
    sanction_all = SanctionList.objects.all()
    qs = SanctionList.objects.all()
    paginator = Paginator(sanction_all, 10)
    page = request.GET.get('page', 1)
    sanctions = paginator.get_page(page)
    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(name__icontains=q)

    page_numbers_range = 10

    max_index = len(paginator.page_range)
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index
    paginator_range = paginator.page_range[start_index:end_index]

    context = {
        'sanctions': sanctions,
        'sanction_list': qs,
        'q': q,
        'paginator_range': paginator_range,
    }
    return render(request, 'sanction/sanction_list.html', context)


def result(request):
    query = request.GET['query']
    if query:
        qs = SanctionList.objects.filter(name__contains=query)
        paginator = Paginator(qs, 10)
        page = request.GET.get('page', 1)
        sanctions = paginator.get_page(page)

        page_numbers_range = 10
        max_index = len(paginator.page_range)
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range

        if end_index >= max_index:
            end_index = max_index
        paginator_range = paginator.page_range[start_index:end_index]

        context = {
            'sanctions': sanctions,
            'sanction_list': qs,
            'paginator_range': paginator_range,
        }
    return render(request, 'sanction/result.html', context)


# Create your views here.
