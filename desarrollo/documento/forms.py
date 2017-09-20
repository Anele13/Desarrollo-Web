from django import forms
import csv, operator

class UploadForm(forms.Form):
    filename = forms.CharField(max_length=100)
    docfile = forms.FileField(label='Selecciona un archivo')
