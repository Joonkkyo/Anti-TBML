from .models import SanctionList
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect
from .forms import SanctionRegistration

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
    q = request.GET.get('q', '')
    qs = SanctionList.objects.filter(name__contains=q)
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
        'q': q,
    }
    return render(request, 'sanction/result.html', context)


def sanction_add(request):
    if request.method == 'POST':
        fm = SanctionRegistration(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            ty = fm.cleaned_data['type']
            pr = fm.cleaned_data['program']
            reg = SanctionList(name=nm, type=ty, program=pr)
            reg.save()
            fm = SanctionRegistration()
    else:
        fm = SanctionRegistration(request.POST)
        sanction_all = SanctionList.objects.all()
    return render(request, 'sanction/sanction_add.html', {'form': fm, 'sanctions': sanction_all})


def sanction_delete(request, id):
    if request.method == 'POST':
        sanction = SanctionList.objects.get(pk=id)
        sanction.delete()
        context = {
            'sanctions': sanction,
        }
        return render(request, 'sanction/sanction_list.html', context)

# def sanction_update(request):
#     return render(request, 'sanction/san')
    # sanction_all = SanctionList.objects.all()
    # context_dict = {'sanctions': sanction_all}
    # return render(request, 'sanction/sanction_add.html', context_dict)
# Create your views here.
