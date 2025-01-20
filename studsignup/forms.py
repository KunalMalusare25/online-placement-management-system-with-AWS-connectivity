from django import forms

from .models import *


class Company(forms.ModelForm):
    class Meta:
        model = Myreg
        fields = ['companyName', 'driveDate', 'link']


