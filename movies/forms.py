from django import forms
from movies.models import *

class UploadFileForm(forms.Form):
    file  = forms.FileField()