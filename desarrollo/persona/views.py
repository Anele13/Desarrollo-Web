#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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


def solo_agente(view):
    def wrap(request):
        try:
            persona = request.user.persona
            if persona.agente:
                if persona.agente and persona.administrador:
                    return redirect('home')
                else:
                    return view(request)
            else:
                return redirect('home')
        except:
                return redirect('mostrar_super_admin')
    return wrap

def solo_administrador(view):
    def wrap(request):
        try:
            persona = request.user.persona
            if persona.administrador:
                return view(request)
            else:
                return redirect('home')
        except:
                return redirect('mostrar_super_admin')
    return wrap

def get_personas_a_cargo(administrador):
    diccionario = {}
    for empresa in Empresa.objects.filter(administrador_Responsable=administrador.id):
        lista_personas=[]
        for persona in PersonaEmp.objects.filter(codemp=empresa.codemp).order_by('documento'):
            lista_personas.append(persona.documento_id)
        diccionario[empresa.codemp]=lista_personas
    return diccionario

@login_required
def home(request):
    try:
        persona = request.user.persona
        if persona.administrador:
            return redirect('mostrar_administrador')
        else:
            return redirect('mostrar_agente')
    except: #Excepcion: usuario no tiene persona
        return redirect('mostrar_super_admin')

@login_required
def cambiar_contraseña(request):
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
    user_list=[]
    lista_empresas=Empresa.objects.filter(administrador_Responsable=request.user.persona.administrador).order_by("codemp")
    safs = PersonaEmp.objects.filter(codemp=request.GET.get('saf')) #enviar nro saf
    user_list = Persona.objects.filter(documento__in=safs.values('documento')).order_by('documento') #"join"
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'persona/administrador.html', {'lista_empresas':lista_empresas, 'lista_personas': user_filter})


@login_required
def reportes_agentes(request):

    lista_saf=Empresa.objects.filter(administrador_Responsable=request.user.persona.administrador).order_by("codemp")

    if request.method =='POST':
        directorio = eg.diropenbox(msg="Abrir directorio:", title="Control: diropenbox")

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


    meses= Mes.objects.filter(id__in=list(set(list(Hliquidac.objects.all().values_list('mes', flat=True)))))

    contexto={'lista_meses':meses,
              'lista_saf':lista_saf,
              }

    return render(request, 'persona/administrador.html', contexto)


@login_required
@solo_agente
def mostrar_agente(request):
    return render(request, 'persona/agente.html')

@login_required
@solo_administrador
def mostrar_administrador(request):
    return render(request, 'persona/administrador.html')

@login_required
def salir(request):
    logout(request)
    return redirect('login')



def liquidacion_final_persona(request, documento):
    contexto = {}
    #return render(request, 'liquidacion/liquidacion_final.html',contexto)
    return render(request, 'persona/administrador.html')
