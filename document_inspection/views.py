from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
#
# class DocumentLV(TemplateView):
#     template_name = "document_inspection/file_upload.html"
#
class ScanLV(TemplateView):
    template_name = "document_inspection/scan.html"

from .models import File
from .forms import FileForm

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
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'document_inspection/upload.html', context)