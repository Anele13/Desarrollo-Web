from django.shortcuts import render
from django.utils.html import format_html
from .models import *
import pandas as pd

def procesar_liq(request, mes=None):
    pass

def liquidaciones(request, mes=None):

    if mes:
        df_mes = pd.DataFrame(list(Mes.objects.all().values()),columns=["id","nombre"])
        df_liquidacion_concepto = pd.DataFrame(list(Concepto.objects.all().filter(ordenliq__isnull=False).values()),columns=["concepto","descrip"])
        df_hliquidac = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=11001005,mes=mes).values()),columns=["concepto_id","mes_id","monto"])
        liquidacion_concepto= df_hliquidac.set_index('concepto_id').join(df_liquidacion_concepto.set_index('concepto')) # Muestra ordenliq =/ NULL
        liquidacion_concepto_mes = liquidacion_concepto.set_index('mes_id').join(df_mes.set_index('id')) # Join con tabla meses para mostrar nombre
        qs=pd.pivot_table(liquidacion_concepto_mes,index=["descrip"], columns=["nombre"], values="monto", fill_value=0)

        df_mes2 = pd.DataFrame(list(Mes.objects.all().values()),columns=["id","nombre"])
        df_liquidacion_concepto2 = pd.DataFrame(list(Concepto.objects.all().filter(ordenliq__isnull=False).values()),columns=["concepto","descrip"])
        df_hliquidac2 = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=11001005).values()),columns=["concepto_id","mes_id","monto"])
        liquidacion_concepto2= df_hliquidac2.set_index('concepto_id').join(df_liquidacion_concepto2.set_index('concepto')) # Muestra ordenliq =/ NULL
        liquidacion_concepto_mes2 = liquidacion_concepto2.set_index('mes_id').join(df_mes2.set_index('id')) # Join con tabla meses para mostrar nombre
        qs2=pd.pivot_table(liquidacion_concepto_mes2,index=["descrip"], columns=["nombre"], values="monto", fill_value=0)

        meses = df_mes2[:(len(qs2.columns))].set_index('id')['nombre'].to_dict()
        resul = format_html(qs.to_html())

    else:
        df_mes = pd.DataFrame(list(Mes.objects.all().values()),columns=["id","nombre"])
        df_liquidacion_concepto = pd.DataFrame(list(Concepto.objects.all().filter(ordenliq__isnull=False).values()),columns=["concepto","descrip"])
        df_hliquidac = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=11001005).values()),columns=["concepto_id","mes_id","monto"])
        liquidacion_concepto= df_hliquidac.set_index('concepto_id').join(df_liquidacion_concepto.set_index('concepto')) # Muestra ordenliq =/ NULL
        liquidacion_concepto_mes = liquidacion_concepto.set_index('mes_id').join(df_mes.set_index('id')) # Join con tabla meses para mostrar nombre
        qs=pd.pivot_table(liquidacion_concepto_mes,index=["descrip"], columns=["nombre"], values="monto", fill_value=0)
        meses = df_mes[:(len(qs.columns))].set_index('id')['nombre'].to_dict()
        resul = format_html(qs.to_html())

    return render(request, 'persona/prueba.html', {'resul':resul, 'meses':meses})
