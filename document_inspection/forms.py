from django import forms
from document_inspection.models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "file_path"]