from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from .models import Image
from .forms import FileForm
#
# class DocumentLV(TemplateView):
#     template_name = "document_inspection/file_upload.html"
#


class ScanLV(TemplateView):
    template_name = "document_inspection/scan.html"


# def showfile(request):
#     lastfile = File.objects.last()
#     file_path = lastfile.file_path
#
#     form = FileForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         form.save()
#
#     context = {
#         'file_path':file_path,
#         'form':form,
#     }
#
#     return render(request, 'document_inspection/file_upload.html', context)


def upload(request):
    context = {}
    if request.method == "POST":
        if request.FILES['document'] is not None:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
            context['uploaded_file'] = uploaded_file
            return render(request, 'document_inspection/upload.html', context)
        else:
            return render(request, 'document_inspection/upload.html')
    return render(request, 'document_inspection/upload.html', context)
