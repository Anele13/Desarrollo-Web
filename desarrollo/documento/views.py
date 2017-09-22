from django.shortcuts import render
from documento.forms import UploadForm
from documento.models import Documento
from django.shortcuts import render, redirect
import os
from sqlalchemy import create_engine
from liquidacion.models import *

def crear():
    engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_economia', pool_recycle=3600)
    lista_a_borrar=['session','migrations', 'group', 'content', 'usuario','permission', 'admin','documento']
    lista=[]
    lista2=[]
    for tabla in engine.table_names():
        codigo=tabla.split('_', 2)
        lista.append(codigo[1])
    for elemento in lista:
        if elemento not in lista_a_borrar:
            lista2.append(elemento)
    return lista2

def baja(request):
    lista=crear()
    return render(request, 'documento/upload.html', {'tablas':lista})

def alta_admin(request):
    empresas=Empresa.objects.all()
    return render(request, 'documento/upload.html', {'empresas': empresas})

def subir_archivo(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Documento(filename = request.POST['tabla'],docfile = request.FILES['docfile'])
            newdoc.save()
            newdoc.csv_to_base(newdoc)
            newdoc.delete()
            if os.path.isfile(newdoc.docfile.path):
                os.remove(newdoc.docfile.path)
            return redirect("uploads")
    else:
        form = UploadForm()
    return render(request, 'documento/upload.html', {'form': form})

def mostrar_super_admin(request):
    return render(request, 'documento/upload.html')
