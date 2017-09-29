from django import forms
import csv, operator

class UploadForm(forms.Form):
    filename = forms.CharField(max_length=100)
    docfile = forms.FileField(label='Selecciona un archivo')

def save(self):    
    csvarchivo = open(self)  # Abrir archivo csv
    entrada = csv.reader(csvarchivo)  # Leer todos los registros
    reg = next(entrada)  # Leer registro (lista)
    print(reg)  # Mostrar registro
