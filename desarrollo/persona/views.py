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

def get_personas_a_cargo(usuario):
    lista_personas = []
    lista2 = PersonaEmp.objects.filter(codemp_id=usuario.persona.administrador.get_empresa())
    for objeto in lista2:
        lista_personas.append(objeto.documento_id)
    #print(connections['default'].queries)
    return lista_personas

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
def mostrar_administrador(request):
    return render(request, 'persona/administrador.html')

@login_required
def agentes_a_cargo(request):
    lista=[]
    administrador= request.user
    lista= get_personas_a_cargo(administrador)
    return render(request, 'persona/agentes_a_cargo.html', {'lista':lista})

@login_required
def mostrar_agente(request):
    return render(request, 'persona/agente.html')

@login_required
def salir(request):
    logout(request)
    return redirect('login')
