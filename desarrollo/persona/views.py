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
from .forms import FormularioIngreso
from liquidacion.models import *
from django.db import connections

def solo_agente(view):
    def wrap(request):
        persona = request.user.persona
        if persona.agente:
            if persona.agente and persona.administrador:
                return redirect('home')
            else:
                return view(request)
        else:
            return redirect('home')
    return wrap

def solo_administrador(view):
    def wrap(request):
        persona = request.user.persona
        if persona.administrador:
            return view(request)
        else:
            return redirect('home')
    return wrap

def get_personas_a_cargo(administrador):
    diccionario = {}
    for empresa in Empresa.objects.filter(administrador_Responsable=administrador.id):
        lista_personas=[]
        for persona in PersonaEmp.objects.filter(codemp=empresa.cod_emp).order_by('documento_id'):
            lista_personas.append(persona.documento_id)
        diccionario[empresa.cod_emp]=lista_personas
    return diccionario

@login_required
def home(request):
    if request.user.persona.administrador:
        return redirect('mostrar_administrador')
    else:
        return redirect('mostrar_agente')

def nuevo_usuario(request):
    if request.method == 'POST':
        form= FormularioIngreso(request.POST)
        if form.is_valid():
            cuil= form.cleaned_data['cuil']
            contraseña= form.cleaned_data['contraseña']
            form.obtener_o_crear(cuil, contraseña)
            return redirect('login')
        else:
            print (form.errors)
    else:
        form= FormularioIngreso()
    return render(request, 'registration/nuevo_usuario.html', {'form': form })

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
    lista=[]
    administrador= request.user.persona.administrador
    lista= get_personas_a_cargo(administrador)
    return render(request, 'persona/administrador.html', {'lista':lista})

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
