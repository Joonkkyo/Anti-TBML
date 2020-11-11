from django import forms
from document_inspection.models import Image


class FileForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file_path']
