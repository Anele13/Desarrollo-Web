from sqlalchemy import create_engine
from django import forms
import csv, operator
from sqlalchemy import create_engine

def crear():
    engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_economia', pool_recycle=3600)
    lista_a_borrar=['session','migrations', 'group', 'content', 'usuario','permission', 'admin','documento']
    lista={}
    lista2=[]
    extra=[]
    for tabla in engine.table_names():
        #codigo=tabla.split('_', 2) #elimina lo que esta al principio de cada nombre de tabla: "liqu_concepto" quedaria solo "concepto"
        lista[tabla]=tabla
    '''for elemento in lista:
        if elemento not in lista_a_borrar:
            lista2.append(elemento)'''
    print (tuple(lista.items()))
    return (tuple(lista.items()))#devolver lista 2 si se descomenta el codigo original!!

class UploadForm(forms.Form):
    tabla= forms.ChoiceField(widget = forms.Select())
    docfile = forms.FileField(label='Selecciona un archivo')

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['tabla'] = forms.ChoiceField(choices=crear())
