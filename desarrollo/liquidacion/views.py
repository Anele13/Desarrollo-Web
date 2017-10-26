from django.shortcuts import render, redirect
from django.utils.html import format_html
from .models import *
import pandas as pd
from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf
from django.contrib.auth.decorators import login_required
from persona import models as pmodels
from persona import views as pviews
from django.core.exceptions import ValidationError
import operator
from django.contrib import messages

def mi_decorador(view):
    def wrap(request, documento=None, mes=None):
        if request.user.persona.administrador and documento:
            diccionario={}
            diccionario= pviews.get_personas_a_cargo(request.user.persona.administrador)
            for key,value in diccionario.items():
                if int(documento) in value:
                    return view(request, documento, mes)
            return redirect('home')
        elif request.user.persona.agente and documento:
            if request.user.persona.documento != int(documento):
                return redirect('home')
            else:
                return view(request, documento, mes)
        else:
            return view(request, documento, mes)
    return wrap


def procesar_liq(documento, df_mes):
    df_liquidacion_concepto = pd.DataFrame(list(Concepto.objects.all().filter(ordenliq__isnull=False).values()),columns=["concepto","descrip","ordenliq"]) # Muestra ordenliq =/ NULL
    df_hliquidac = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=documento).values()),columns=["concepto_id","mes_id","monto"])
    liquidacion_concepto= df_hliquidac.set_index('concepto_id').join(df_liquidacion_concepto.set_index('concepto')) # Conceptos que estan en la liquidación
    liquidacion_concepto_mes = liquidacion_concepto.set_index('mes_id').join(df_mes.set_index('id')) # Join con tabla meses para mostrar nombre
    qs=pd.pivot_table(liquidacion_concepto_mes,index=["ordenliq","descrip"], columns="nombre", values="monto", fill_value=0).reset_index('ordenliq')
    qs.__delitem__('ordenliq')  #borra la columna ordenliq
    qs.index.name = None        # elimina la fila en blanco (descrip)
    return qs

def extra(documento):
    df_mes = pd.DataFrame(list(Mes.objects.all().values()),columns=["id","nombre"])
    qs = procesar_liq(documento, df_mes)
    return qs

def achicar(qs, lista_extra=None):
    if lista_extra:
        qs = qs[lista_extra] #Reordena la tabla por mes
    return qs

def ordenar_nombre_meses(qs):
    diccionario = {}
    lista=[]
    for mes in qs.columns:
        if Mes.objects.filter(nombre=mes):
            diccionario[Mes.objects.get(nombre=mes).id]=mes
    for key, value in dict((key,value) for key,value in sorted(diccionario.items(), key=operator.itemgetter(0))).items():
        lista.append(value)
    qs = qs[lista] #Reordena la tabla por mes
    return qs

def color_negative_red(val):
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

def hover(hover_color="#ffff99"):
    return dict(selector="tr:hover",
                props=[("background-color", "%s" % hover_color)])

styles = [
    hover(),
    dict(selector="th", props=[("font-size", "90%"),
                               ("text-align", "left"),
                               ("font-family", "Verdana"),
                               ("background-color", "#cccccc"),
                               ("font-weight", "Bold"),
                               ("text-transform", "capitalize")]),

    dict(selector="tr", props=[("font-size", "90%"),
                                ("text-align", "right"),
                                ("font-family", "Verdana"),
                                ("background-color", "#ffffff")])
]


@login_required
@mi_decorador
def liquidaciones(request, documento=None, mes=None):
    tabla = []
    meses = []
    contexto={}

    doc=request.user.persona.documento # del que está loggeado.
    if documento: # si hay documento es un admin queriendo ver la liquidacion de un agente
        doc=documento
    if not Hliquidac.objects.filter(documento=doc):
        messages.add_message(request, messages.WARNING, 'La persona no posee liquidaciones.')
    else:
        nombre_persona = pmodels.Persona.objects.get(documento=doc).nya
        qs1= extra(doc)
        qs1= ordenar_nombre_meses(qs1)
        meses=list(qs1.columns)
        qs1=achicar(qs1,request.POST.getlist("check"))
        tabla=qs1.style.set_table_styles(styles).applymap(color_negative_red).format("{:,.2f}").render()

        contexto={  'nombre_persona':nombre_persona,
                    'tabla':tabla,
                    'meses':meses,
                    'doc':doc,}
    if request.user.persona.administrador:
        return render(request, 'persona/administrador.html',contexto)
    return render(request, 'persona/agente.html', contexto)


class PdfLiquidacion(PDFTemplateView):
    template_name = 'liquidacion/liquidacion_pdf.html'
    title = "Planilla de Liquidación de Impuesto  a las Ganancias"

    def datos_agente(self,**kwargs):
        doc_usuario= self.request.user.persona.documento
        if 'documento' in self.kwargs:
            doc_usuario = self.kwargs['documento']

        persona = pmodels.Persona.objects.get(documento=doc_usuario)
        datos = {'Nombre': persona.nya, 'Cuil':persona.cuil, 'Fecha f572':persona.fechaf572,
                'Fecha ult. presentación Web': persona.fechaweb, 'Nº presentacion':persona.nropres}
        return datos

    def imprimir_liq(self,**kwargs):
        doc_usuario= self.request.user.persona.documento
        if 'documento' in self.kwargs:
            doc_usuario = self.kwargs['documento']
        qs1 = extra(doc_usuario)
        qs1= ordenar_nombre_meses(qs1)
        resul=qs1.style.set_table_styles(styles).format("{:,.2f}").render()
        return resul
