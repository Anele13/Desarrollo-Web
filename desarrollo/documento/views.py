from django.shortcuts import render
from documento.forms import UploadForm
from documento.models import Documento
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from sqlalchemy import create_engine
from liquidacion.models import *
from persona.models import *
from django.contrib import messages
from django.core.exceptions import ValidationError
import easygui as eg
from .models import *
from django.core.files import File
from django.views.generic.edit import FormView
from django.http import HttpResponse

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
    empresas=Empresa.objects.all()
    lista=Persona.objects.all()
    if request.method == 'POST':
        if not Persona.objects.filter(documento=request.POST.get('documento')).exists():
            messages.add_message(request, messages.WARNING, 'No existe el documento ingresado.')
        else:
            admin= obtener_o_crear_admin(request.POST.get('documento'))
            persona= Persona.objects.get(documento=request.POST.get('documento'))
            empresa= Empresa.objects.get(codemp=request.POST.get('empresa'))
            empresa.administrador_Responsable=admin
            persona.administrador= admin
            empresa.save()
            persona.save()
            return redirect("mostrar_super_admin")
    return render(request, 'documento/upload.html', {'empresas': empresas})

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


@solo_super_admin
@login_required
def presentacion_f572(request):
    directorio = eg.fileopenbox(msg="Abrir directorio:",filetypes="*.pdf", multiple=True, title="Control: diropenbox")

    for path in directorio:
        f572 = open(path,'rb')
        path= path.split("\\")
        tipo = ""
        try:
            cuil,periodo,presentacion, nropres, tipo = path[len(path)-1].split("_")# tipo pres:B
        except:
            cuil,periodo,presentacion, nropres = path[len(path)-1].split("_")# tipo pres:A


        archivo = Pdf572(cuil=int(cuil),
                        periodo=int(periodo),
                        presentacion=int(nropres.split(".")[0]),
                        docfile=File(f572))

        archivo.docfile.save(cuil +"-"+ nropres.split(".")[0] +"-"+ tipo.split(".")[0] + ".pdf",File(f572))
        archivo.save()

    return render(request, 'presentacionf572/presentacion_f572.html')


def pdf_form572(request, cuil):

    cuil_persona = "".join(cuil.split("-"))

    lista_pdf = Pdf572.objects.filter(cuil=int(cuil_persona)).order_by('presentacion')

    '''
    si esta el b muestra solo b
    agente: periodo, nropres, cuil (si es a o b sale de cuilreten)
    '''

    if lista_pdf :
        resul = lista_pdf[len(lista_pdf)-1].docfile.path # solo se muestra el último
        rr = resul.replace("\\", "/")
        image_data = open(rr, "rb").read()
        return HttpResponse(image_data, content_type="application/pdf")

    else:
        messages.error(request,"La persona no posee formulario 572")
        return redirect('home')
