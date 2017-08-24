#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import FormularioUsuario
from django.contrib import messages


@login_required
def home(request):
    return render(request, 'base/home.html')

def signup(request):
    if request.method == 'POST':
        form = FormularioUsuario(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('cuil')
            contrasenia = form.cleaned_data.get('contraseña')
            usuario= FormularioUsuario.obtener_o_crear(username, contrasenia)
            return redirect('home')
    else:
        form = FormularioUsuario()
    return render(request, 'registration/signup.html', {'form': form})
