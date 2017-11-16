from django.shortcuts import render
from documento.forms import UploadForm
from documento.models import Documento
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from sqlalchemy import create_engine
from liquidacion.models import *
from persona.models import *
from persona import views as pviews
from django.contrib import messages
from django.core.exceptions import ValidationError
import easygui as eg
from .models import *
from django.core.files import File
from django.views.generic.edit import FormView
from django.http import HttpResponse
from liquidacion.views import mi_decorador

def solo_super_admin(view):
    def wrap(request):
        '''
        Decorador Solo super admin:
        Se encarga de devolver la vista solicitada solamente al super administrador.
        :param request: Requerimiento HTTP, el super administrador existe en el sistema.
        :return: Se devuelve la vista correspondiente.
        '''
        try:
            persona= request.user.persona
            if persona.administrador:
                return redirect('mostrar_administrador')
            else:
                return redirect('mostrar_agente')
        except:
            return view(request)
    return wrap


@login_required
@solo_super_admin
def mostrar_super_admin(request):
    '''
    Función mostrar super admin:
    Se encarga de devolver la vista solicitada solamente al super administrador.
    :param request: Requerimiento HTTP, el super administrador existe en el sistema.
    :return: Se devuelve la vista correspondiente.
    '''
    return render(request, 'documento/upload.html')


def obtener_o_crear_admin(doc):
    '''
    Función obtener o crear admin:
    Se encarga de verificar los datos del administrador, si no existe, se crea.
    :param doc: Documento ingresado por el administrador.
    :return: Devuelve el usuario de la persona.
    '''
    admin=Persona.objects.get(documento=doc).administrador
    if admin:
        return admin
    else:
        return Administrador()

@login_required
@solo_super_admin
def alta_admin(request):
    '''
    Función alta admin:
    Se encarga de asignar un administrador a un SAF.
    :param request: Requerimiento HTTP.
    :return: Devuelve la vista correspondiente luego de dar de alta el administrador.
    '''
    empresas=Empresa.objects.all()
    lista=Persona.objects.all()
    if request.method == 'POST':
        if not Persona.objects.filter(documento=request.POST.get('documento')).exists():
            messages.add_message(request, messages.WARNING, 'No existe el documento ingresado.')
        else:
            admin= obtener_o_crear_admin(request.POST.get('documento'))
            admin.save()
            persona= Persona.objects.get(documento=request.POST.get('documento'))
            empresa= Empresa.objects.get(codemp=request.POST.get('empresa'))
            empresa.administrador_Responsable=admin
            persona.administrador= admin
            empresa.save()
            persona.save()
            messages.success(request,"se ha dado de alta un nuevo administrador")
            return redirect("mostrar_super_admin")
    return render(request, 'documento/upload.html', {'empresas': empresas})

@solo_super_admin
@login_required
def subir_archivo(request):
    '''
    Función subir archivo:
    Se encarga de asigar a la DB los datos contemplados en el archivo CSV.
    :param request: Requerimiento HTTP.
    :return: Devuelve la vista correspondiente luego de cargar el archivo.
    '''
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Documento(filename = request.POST['tabla'],docfile = request.FILES['docfile'])
            newdoc.save()
            try:
                newdoc.csv_to_base(newdoc)
                newdoc.delete()
                if os.path.isfile(newdoc.docfile.path):
                    os.remove(newdoc.docfile.path)
                    messages.success(request,"se han actualizado los datos de la tabla solicitada")
                    return redirect("mostrar_super_admin")
            except Exception as e:
                print(e)
                messages.add_message(request, messages.WARNING,'Error de carga en el archivo')
                return redirect("mostrar_super_admin")
    else:
        form = UploadForm()
    return render(request, 'documento/upload.html', {'form': form})


@solo_super_admin
@login_required
def presentacion_f572(request):
    '''
    Función presentación f572:
    Se encarga de asigar a la DB los datos contemplados en el formulario 572.
    :param request: Requerimiento HTTP.
    :return: Devuelve la vista correspondiente luego de cargar el formulario 572.
    '''
    directorio = eg.fileopenbox(msg="Abrir directorio:",filetypes="*.pdf", multiple=True, title="Control: diropenbox")
    lista_pdf = Pdf572.objects.all()
    if lista_pdf:
        for pdf in lista_pdf:
            os.remove(pdf.docfile.path)
            pdf.delete()

    if directorio:
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
                            docfile=File(f572),
                            tipo=tipo.split('.')[0]) # solamente la letra b si es de ese tipo

            archivo.docfile.save(cuil +"-"+ nropres.split(".")[0] +"-"+ tipo.split(".")[0] + ".pdf",File(f572))
            archivo.save()
        messages.success(request,"se han cargado un total de: " +str(len(Pdf572.objects.all()))+ " formularios 572")
    return redirect('mostrar_super_admin')

@login_required
def pdf_form572(request, cuil):
    '''
    Función pdf form 572:
    Se encarga de enviar los datos del form 572 para mostrar en PDF.
    :param request: Requerimiento HTTP.
    :param cuil: Cuil de la persona existe en el sistema.
    :return: Devuelve la vista correspondiente mostrando la información en el PDF.
    '''
    persona = pviews.Persona.objects.get(cuil=cuil)
    cuil_persona = "".join(cuil.split("-"))
    try:
        if persona.wcuitreten == '0': # no tiene agente retencion
            f572 = Pdf572.objects.get(cuil=int(cuil_persona), periodo=persona.periodo, presentacion=persona.nropres, tipo="")
        else:
            f572 = Pdf572.objects.get(cuil=int(cuil_persona), periodo=persona.periodo, presentacion=persona.nropres, tipo="b")
        resul = f572.docfile.path
        rr = resul.replace("\\", "/")
        image_data = open(rr, "rb").read()
        return HttpResponse(image_data, content_type="application/pdf")
    except:
        messages.error(request,"La persona no registra formulario 572")
        return redirect('home')
