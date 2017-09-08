from django.shortcuts import render
from django.utils.html import format_html
from .models import *
import pandas as pd
from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf

#11261198

def procesar_liq(documento, mes, df_mes):
    # SI NO ES NECESARIO UTILIZAR EL MES, SE AGREGA CERO.
    df_liquidacion_concepto = pd.DataFrame(list(Concepto.objects.all().filter(ordenliq__isnull=False).values()),columns=["concepto","descrip","ordenliq"])

    if mes != 0:
        df_hliquidac = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=documento,mes=mes).values()),columns=["concepto_id","mes_id","monto"])
    else:
        df_hliquidac = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=documento).values()),columns=["concepto_id","mes_id","monto"])

    liquidacion_concepto= df_hliquidac.set_index('concepto_id').join(df_liquidacion_concepto.set_index('concepto')) # Muestra ordenliq =/ NULL
    liquidacion_concepto_mes = liquidacion_concepto.set_index('mes_id').join(df_mes.set_index('id')) # Join con tabla meses para mostrar nombre
    qs=pd.pivot_table(liquidacion_concepto_mes,index=["ordenliq","descrip"], columns="nombre", values="monto", fill_value=0)
    qs.index.names = [None,None]
    #qs.index.name = None,
    return qs

def extra(documento, mes=None):
    df_mes = pd.DataFrame(list(Mes.objects.all().values()),columns=["id","nombre"])

    if mes:
        qs = procesar_liq(documento, mes, df_mes)
    else:
        qs = procesar_liq(documento, 0, df_mes)
        meses = df_mes[:(len(qs.columns))].set_index('id')['nombre'].to_dict()
        qs = qs.reindex_axis(list(meses.values())[:(len(qs.columns))], axis=1) # toma los meses que hay en la lista
    return qs


def liquidaciones(request, documento=None, mes=None):
    doc=request.user.persona.documento
    documentos=None
    if documento:
        doc=documento
        documentos=documento
    qs1= extra(doc, mes)
    qs2= extra(doc)
    df_mes = pd.DataFrame(list(Mes.objects.all().values()),columns=["id","nombre"])
    meses = df_mes[:(len(qs2.columns))].set_index('id')['nombre'].to_dict()
    qs2 = qs2.reindex_axis(list(meses.values())[:(len(qs2.columns))], axis=1) # toma los meses que hay en la lista
    resul = format_html(qs1.to_html())
    return render(request, 'persona/prueba.html', {'resul':resul, 'meses':meses, 'documentos':documentos})


class PdfLiquidacion(PDFTemplateView):
    template_name = 'liquidacion/liquidacion_pdf.html'
    title = "Mis liquidaciones"

    def procesar_liq(self):
        doc_usuario = self.request.user.persona.documento
        resul = format_html(extra(doc_usuario).to_html())
        return resul
