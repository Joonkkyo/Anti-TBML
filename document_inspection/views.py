from django.views.generic import TemplateView

# Create your views here.

class DocumentLV(TemplateView):
    template_name = "document_inspection/file_upload.html"

class ScanLV(TemplateView):
    template_name = "document_inspection/scan.html"