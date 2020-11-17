from django import forms
from .models import SanctionList


class SanctionRegistration(forms.ModelForm):
    class Meta:
        model = SanctionList
        fields = ['name', 'type', 'program']


class SanctionUpdate(forms.ModelForm):
    class Meta:
        model = SanctionList
        fields = ['name', 'type', 'program']
