#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import FormularioUsuario
from django.contrib.auth import logout
from django.forms import ValidationError
from persona.models import *
from django.contrib import messages
from .forms import *
from liquidacion.models import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .filters import *
import pandas as pd
import easygui as eg
import xlsxwriter
from django.utils.timezone import now

def home(request):
    '''
    Función Home:
    Se encarga de mostrar la pagina principal, de acuerdo al usuario que inició sesión.
    :param request: Requerimiento HTTP, la persona existe en el sistema.
    :return: Se devuelve la vista correspondiente.
    '''
    try:
        persona = request.user.persona
        if persona.administrador:
            return redirect('mostrar_administrador')
        else:
            return redirect('mostrar_agente')
    except:
            return redirect('mostrar_super_admin')


def solo_agente(view):
    def wrap(request):
        '''
        Decorador Solo Agente:
        Se encarga de devolver la vista solicitada solamente al agente.
        :param request: Requerimiento HTTP, la persona existe en el sistema.
        :return: Se devuelve la vista correspondiente.
        '''
        try:
            persona=request.user.persona
            if persona.administrador:
                return redirect('mostrar_administrador')
            else:
                return view(request)
        except:
                return redirect('mostrar_super_admin')
    return wrap

def solo_administrador(view):
    def wrap(request):
        '''
        Decorador Solo Administrador:
        Se encarga de devolver la vista solicitada solamente al administrador.
        :param request: Requerimiento HTTP, la persona existe en el sistema.
        :return: Se devuelve la vista correspondiente.
        '''
        try:
            persona=request.user.persona
            if persona.agente and not persona.administrador:
                return redirect('mostrar_agente')
            else:
                return view(request)
        except:
                return redirect('mostrar_super_admin')
    return wrap

def get_personas_a_cargo(administrador):
    '''
    Función Get personas a cargo:
    Se encarga de devolver las personas de cada saf que tiene a cargo el administrador.
    :param administrador: Existe un Administrador Responsable.
    :return: Devuelve un diccionario con las personas pertenecientes a cada saf.
    '''
    diccionario = {}
    for empresa in Empresa.objects.filter(administrador_Responsable=administrador.id):
        lista_personas=[]
        for persona in PersonaEmp.objects.filter(codemp=empresa.codemp).order_by('documento'):
            lista_personas.append(persona.documento_id)
        diccionario[empresa.codemp]=lista_personas
    return diccionario

@login_required
def cambiar_contraseña(request):
    '''
    Función cambiar contraseña:
    Es la responsable de cambiar la contraseña del usuario.
    :param request: Requerimiento HTTP, la persona ingresa contraseña antigua.
    :return: El usuario posee la contraseña actualizada.
    '''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'La contraseña fue actualizada correctamente!')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrija los errores señalados.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})

def nuevo_usuario(request):
    '''
    Función nuevo usuario:
    Es la encargada de crear un nuevo usuario en el sistema.
    :param request: Requerimiento HTTP, el usuario existe en el sistema.
    :return: Nuevo usuario creado en el sistema.
    '''
    error = None
    if request.method == 'POST':
        form= FormularioIngreso(request.POST)
        if form.is_valid():
            cuil= form.cleaned_data['cuil']
            usuario = CuilClave.objects.get(cuil=cuil)
            form.obtener_o_crear(cuil, usuario.clave)
            return redirect('login')
        else:
            print (form.errors)
    else:
        form= FormularioIngreso()
    return render(request, 'registration/nuevo_usuario.html', {'form': form , 'error': error})

def login_usuario(request):
    '''
    Función Login usuario:
    Es la responsable de permitir el acceso al sistema del usuario.
    :param request: Requerimiento HTTP, el usuario existe en el sistema.
    :return: El usuario ingresa al sistema.

    '''
    if request.method == 'POST':
        form = FormularioUsuario(data=request.POST)
        if form.is_valid():
            usuario= Usuario.objects.get(username=form.cleaned_data['username'])
            login(request, usuario)
            return redirect('home')
    else:
        form = FormularioUsuario()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def agentes_a_cargo(request):
    '''
    Función Agentes a cargo:
    Se encarga de devolver la lista de agentes y de empresas que posee el administradora cargo.
    :param request: Requerimiento HTTP, el administrador responsable existe en el sistema.
    :return: Devuelve lista de empresas (SAF) y agentes.
    '''
    user_list=[]
    lista_empresas=Empresa.objects.filter(administrador_Responsable=request.user.persona.administrador).order_by("codemp")
    safs = PersonaEmp.objects.filter(codemp=request.GET.get('saf')) #enviar nro saf
    user_list = Persona.objects.filter(documento__in=safs.values('documento')).order_by('documento') #"join"
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'persona/administrador.html', {'lista_empresas':lista_empresas, 'lista_personas': user_filter})


@login_required
def reportes_agentes(request):
    '''
    Función Reportes agentes:
    Es la responsable de generar reportes en excel de la planilla de liquidaciones en un perido determinado.
    :param request: Requerimiento HTTP, el administrador responsable y el SAF existe en el sistema.
    :return: Devuelve un archivo en formato .xlsx.

    '''
    lista_saf=Empresa.objects.filter(administrador_Responsable=request.user.persona.administrador).order_by("codemp")
    if request.method =='POST':
        directorio = eg.diropenbox(msg="Seleccionar Carpeta:", title="Control: diropenbox")
        if directorio:
            nro_saf = request.POST.get('saf')
            nro_mes = request.POST.get('mes')
            df_personas = pd.DataFrame(list(Persona.objects.all().values()),columns=["documento", "nya","nropres","fechapres","fechaweb"])
            df_persona_emp = pd.DataFrame(list(PersonaEmp.objects.all().filter(codemp=nro_saf).values('documento')),columns=["documento"])
            personas_del_saf = pd.merge(df_personas, df_persona_emp, on='documento')
            df_hliquidac = pd.DataFrame(list(Hliquidac.objects.all().filter(mes=nro_mes).values('documento','concepto','monto')),columns=["documento","concepto","monto"])
            liquidacion_personas = pd.merge(personas_del_saf, df_hliquidac, on='documento')
            df_liquidacion_concepto = pd.DataFrame(list(Concepto.objects.all().values()),columns=["concepto","descrip"])
            liquidacion_concepto = pd.merge(liquidacion_personas, df_liquidacion_concepto, on='concepto')
            qs=pd.pivot_table(liquidacion_concepto,index=["documento"], columns=["descrip"], values="monto", fill_value=0).reset_index(col_level=0)# col level para que no se superponga descrip
            final = pd.merge(personas_del_saf, qs, on='documento') # agregado de las columnas nropres, fechapres y fechaweb faltantes en el pivot
            writer = pd.ExcelWriter(directorio+'/prueba.xlsx', engine='xlsxwriter')
            final.to_excel(writer,sheet_name='Reportes', startrow=2) # startrow: despues de agregar los titulos.
            # Get the xlsxwriter workbook and worksheet objects.
            workbook  = writer.book
            worksheet = writer.sheets['Reportes']
            worksheet.set_column(1, len(final.columns), 30)
            formato_titulo = workbook.add_format({'bold': True,'valign': 'top'})
            worksheet.write('B1', "Planilla de Liquidación de impuesto a las Ganancias",formato_titulo) # fila-columna
            worksheet.write('B2', "SAF: "+str(Empresa.objects.get(codemp=nro_saf).codemp)+"-"+str(Empresa.objects.get(codemp=nro_saf).descrip)+", " \
            +"Periodo: "+ Mes.objects.get(id=nro_mes).nombre +"/"+ str(now().year), formato_titulo) # fila-columna
            worksheet.autofilter('B3:F3') #Agrega filtros: documento, nya, nropres, fechapres, fechaweb
            messages.success(request, "Se ha exportado correctamente el archivo excel.")
    meses= Mes.objects.filter(id__in=list(set(Hliquidac.objects.all().values_list('mes', flat=True).distinct())))
    contexto={'lista_meses':meses, 'lista_saf':lista_saf}
    return render(request, 'persona/administrador.html', contexto)


@login_required
def liquidacion_final_persona(request, periodo):
    '''
    Función liquidacion final persona:
    Devuelve  la liquidacion final del agente que la solicitó.
    :param request: Requerimiento HTTP.
    :param periodo: Existe un perido para visualizar.
    :return: La planilla de liquidacion final del agente.
    '''
    liqfin=None
    dict_datos={}
    try:
        liqfin = LiqFin.objects.get(periodo=periodo, documento= request.user.persona.documento)
        for l in liqfin.__dict__.keys():
            try:
                concepto = Concepto.objects.get(fliqfin=l.upper()) # debe estar en mayuscula pra encontrar en la DB
                monto=getattr(liqfin,l)
                dict_datos[concepto.descrip]=monto
            except:
                pass
        dict_datos["Saldo"]=liqfin.saldo
        dict_datos["Saldo a favor de AFIP"]=liqfin.saldoafip
        dict_datos["Saldo a favor de Beneficiario"]=liqfin.saldoben
    except:
        messages.warning(request, "La persona no posee liquidaciones finales")
    if request.user.persona.administrador:
        return render(request, 'persona/administrador.html',{'dict_datos':dict_datos, 'liqfin':liqfin})
    return render(request, 'persona/agente.html',{'dict_datos':dict_datos, 'liqfin':liqfin})


@login_required
@solo_agente
def mostrar_agente(request):
    '''
    Función mostrar agente:
    Devuelve la vista del agente en el sistema.
    :param request: Requerimiento HTTP, existe un agente en el sistema.
    :return: Devuelve la vista del agente.
    '''
    return render(request, 'persona/agente.html')

@login_required
@solo_administrador
def mostrar_administrador(request):
    '''
    Función mostrar administrador:
    Devuelve la vista del administrador en el sistema.
    :param request: Requerimiento HTTP, Existe un administrador en el sistema.
    :return: Devuelve la vista del administrador.
    '''
    return render(request, 'persona/administrador.html')

@login_required
def salir(request):
    '''
    Función salir:
    Se encarga de cerrar la sesión del usuario. Devuelve la vista del login en el sistema.
    :param request: Requerimiento HTTP, Existe un usuario en el sistema.
    :return: Devuelve la vista del login.
    '''
    logout(request)
    return redirect('login')
