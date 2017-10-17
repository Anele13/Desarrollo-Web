from django.shortcuts import render
from documento.forms import UploadForm
from documento.models import Documento
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from sqlalchemy import create_engine
from liquidacion.models import *
from persona.models import *
from django.forms import ValidationError

def solo_super_admin(view):
    def wrap(request):
        try:
            if request.user.persona:
                return redirect('home')
        except:
                return view(request)
    return wrap

@solo_super_admin
@login_required
def crear():
    engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_PRUEBA', pool_recycle=3600)
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

@solo_super_admin
@login_required
def obtener_o_crear_admin(doc):
    admin=Persona.objects.get(documento=doc).administrador
    if admin:
        return admin
    else:
        return Administrador()

@solo_super_admin
@login_required
def alta_admin(request):
    error=0
    empresas=Empresa.objects.all()
    lista=Persona.objects.all()
    if request.method == 'POST':
        if not Persona.objects.filter(documento=request.POST.get('documento')).exists():
            error=1
            print("nada")
        else:
            admin= obtener_o_crear_admin(request.POST.get('documento'))
            persona= Persona.objects.get(documento=request.POST.get('documento'))
            empresa= Empresa.objects.get(codemp=request.POST.get('empresa'))
            empresa.administrador_Responsable=admin
            persona.administrador= admin
            empresa.save()
            persona.save()
            return redirect("mostrar_super_admin")
    return render(request, 'documento/upload.html', {'empresas': empresas, 'error':error})

@solo_super_admin
@login_required
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
            return redirect("mostrar_super_admin")
        else:
            print(form.errors)
    else:
        form = UploadForm()
    return render(request, 'documento/upload.html', {'form': form})

@solo_super_admin
@login_required
def mostrar_super_admin(request):
    return render(request, 'documento/upload.html')
