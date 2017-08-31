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
<<<<<<< HEAD
            username = form.cleaned_data.get('cuil')
            contraseña = form.cleaned_data.get('contraseña')
            usuario= form.obtener_o_crear(username, contraseña)
            login(request, usuario)                        
            return redirect('mostrar_agente')
    else:
        form = FormularioUsuario()
    return render(request, 'registration/login.html', {'form': form})

=======
            usuario= Usuario.objects.get(username=form.cleaned_data['username'])
            login(request, usuario)
            return redirect('home')
    else:
        form = FormularioUsuario()
    return render(request, 'registration/login.html', {'form': form})
>>>>>>> refs/remotes/origin/master

@login_required
def mostrar_agente(request):
    return render(request, 'persona/agente.html')

@login_required
def mostrar_administrador(request):
    return render(request, 'persona/administrador.html')

@login_required
def salir(request):
    logout(request)
    return redirect('login')
