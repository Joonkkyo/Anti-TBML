from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from document_inspection.GOOGLE_VER3 import api_main


class ScanLV(TemplateView):
    template_name = "document_inspection/scan.html"


def upload(request):
    context = {}
    if request.method == "POST":
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        print(fs.path(uploaded_file.name))
        output_image = api_main(fs.path(uploaded_file.name))
        print(output_image)
        context['url'] = fs.url(output_image)

    return render(request, 'document_inspection/upload.html', context)
