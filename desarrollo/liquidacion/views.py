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
import datetime
from django.utils.decorators import method_decorator

def mi_decorador(view):
    def wrap(request, documento=None, mes=None):
        '''
        Función mi Decorador (wrap)
        Se encarga que un administrador no pueda ver liquidaciones de agentes que no pertenecen a su SAF.
        :param request: Requerimiento HTTP
        :param documento: Persona registrada en el sistema
        :param mes: Mes para visualizar la liquidación
        :return: Develve la vista correspondiente
        '''
        if request.user.persona.administrador and documento:
            diccionario={}
            diccionario= pviews.get_personas_a_cargo(request.user.persona.administrador)
            #REFACTOR: OPTIMIZAR BUSQUEDA DE PERSONAS A CARGO.
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
    '''
    Función procesar_liq:
    Es la responsable de crear el queryset (objeto resultado de una consulta a la base) de la liquidación.
    :param documento: Existe documento de la persona en el sistema.
    :param df_mes: DataFrame Mes, para mostrar el nombre de los meses en la tabla liquidación.
    :return: El qs resultante de la liquidación.
    '''
    df_liquidacion_concepto = pd.DataFrame(list(Concepto.objects.all().filter(ordenliq__isnull=False).values()),columns=["concepto","descrip","ordenliq"]) # Muestra ordenliq =/ NULL
    df_hliquidac = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=documento).values()),columns=["concepto_id","mes_id","monto"])
    liquidacion_concepto= df_hliquidac.set_index('concepto_id').join(df_liquidacion_concepto.set_index('concepto')) # Conceptos que estan en la liquidación
    liquidacion_concepto_mes = liquidacion_concepto.set_index('mes_id').join(df_mes.set_index('id')) # Join con tabla meses para mostrar nombre
    qs=pd.pivot_table(liquidacion_concepto_mes,index=["ordenliq","descrip"], columns="nombre", values="monto", fill_value=0).reset_index('ordenliq')
    qs.__delitem__('ordenliq')  #borra la columna ordenliq
    qs.index.name = None        # elimina la fila en blanco (descrip)
    return qs

def extra(documento):
    '''
    Función extra:
    Es la responsable de añadir el DataFrame para la liquidación.
    :param documento: Existe documento de la persona en el sistema.
    :return: El qs resultante de la liquidación.
    '''
    df_mes = pd.DataFrame(list(Mes.objects.all().values()),columns=["id","nombre"])
    qs = procesar_liq(documento, df_mes)
    return qs

def achicar(qs, lista_extra=None):
    '''
    Función achicar:
    Es la responsable de filtrar el qs de la tabla de liquidación.
    :param qs: Existe queryset de liquidacion.
    :param lista_extra: Contiene todos los meses que se deben filtrar.
    :return: El qs filtrado.
    '''
    if lista_extra:
        qs = qs[lista_extra] #Reordena la tabla por mes
    return qs

def ordenar_nombre_meses(qs):
    '''
    Función ordenar nombre meses:
    Es la responsable de reodernar el qs de la tabla de liquidación.
    :param qs: Existe queryset de liquidacion.
    :return: El qs re-ordenado por los meses.
    '''
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
    '''
    Función color rojo negativo:
    Es la responsable de setear en color rojo los números negativos en la tabla de liquidación.
    :param val: Existe valor en la tabla de liquidacion.
    :return: El color del valor correspondiente.
    '''
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

def hover(hover_color="#ffff99"):
    '''
    Función hover:
    Es la responsable de agregar el estilo a la tabla de liquidación.
    :param hover_color: color de la linea seleccionada en la tabla de liquidacion.
    :return: Devuelve tabla de liquidación con estilo hover.
    '''
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
    '''
    Función liquidaciones:
    Es la responsable de visualizar la liquidación correspondiente de la persona.
    :param request: Requerimiento HTTP.
    :param documento: Existe el documento de la persona en el sistema.
    :param mes: Existe un mes para filtrar o pueden ser todos los meses.
    :return: Devuelve tabla de liquidación de la persona.
    '''
    tabla = []
    meses = []
    contexto={}

    doc=request.user.persona.documento # del que está loggeado.
    if documento: # si hay documento es un admin queriendo ver la liquidacion de un agente
        doc=documento
    if not Hliquidac.objects.filter(documento=doc):
        messages.add_message(request, messages.WARNING, 'La persona no posee liquidaciones.')
    else:
        persona = pmodels.Persona.objects.get(documento=doc)
        qs1= extra(doc)
        qs1= ordenar_nombre_meses(qs1)
        meses=list(qs1.columns)
        qs1=achicar(qs1,request.POST.getlist("check"))
        tabla=qs1.style.set_table_styles(styles).applymap(color_negative_red).format("{:,.2f}").render()

        año_liq = (datetime.date.today().year)
        año_anterior = año_liq - 1

        contexto={  'persona':persona,
                    'tabla':tabla,
                    'meses':meses,
                    'doc':doc,
                    'año_liq':año_liq,
                    'año_anterior':año_anterior}

    if request.user.persona.administrador:
        return render(request, 'persona/administrador.html',contexto)
    return render(request, 'persona/agente.html', contexto)


class PdfLiquidacion(PDFTemplateView):
    '''
    Clase PdfLiquidacion:
    Esta clase se encarga de generar un template para transformarlo a PDF.
    '''
    template_name = 'liquidacion/liquidacion_pdf.html'
    title = "Planilla de Liquidación de Impuesto  a las Ganancias"

    @method_decorator(login_required)
    @method_decorator(mi_decorador)
    def dispatch(self, *args, **kwargs):
        '''
        Función dispatch:
        Responsable de devolver la vista correspondiente a la persona que lo solicitó.
        :param args: Argumentos que podrían llegar a venir en la llamada.
        :param kwargs: Mas argumentos.
        :return: Devuelve vista dependiendo del usuario.
        '''
        return super(PDFTemplateView, self).dispatch(*args, **kwargs)

    def datos_agente(self,**kwargs):
        '''
        Función datos agente:
        Responsable de devolver los datos del agente para mostrar en el PDF.
        :param self: Existe el objeto creado.
        :param kwargs: Datos del agente.
        :return: Devuelve los datos del usuario.
        '''
        doc_usuario= self.request.user.persona.documento
        if 'documento' in self.kwargs:
            doc_usuario = self.kwargs['documento']

        persona = pmodels.Persona.objects.get(documento=doc_usuario)
        datos = {'Nombre': persona.nya, 'Cuil':persona.cuil, 'Fecha f572':persona.fechaf572,
                'Fecha ult. presentación Web': persona.fechaweb, 'Nº presentacion':persona.nropres}
        return datos

    def imprimir_liq(self,**kwargs):
        '''
        Función imprimir liquidación:
        Responsable de enviar la tabla de liquidación para mostrar en el PDF.
        :param self: Existe el objeto creado.
        :param kwargs: Datos del agente.
        :return: Envia la tabla de liquidación en formato PDF.
        '''
        doc_usuario= self.request.user.persona.documento
        if 'documento' in self.kwargs:
            doc_usuario = self.kwargs['documento']
        qs1 = extra(doc_usuario)
        qs1= ordenar_nombre_meses(qs1)
        resul=qs1.style.set_table_styles(styles).format("{:,.2f}").render()
        return resul
