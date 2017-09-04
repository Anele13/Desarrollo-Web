from django.shortcuts import render
from django.utils.html import format_html
from .models import *
import pandas as pd

def liquidaciones(request):
    return render(request, 'persona/prueba.html')

def extra(request, mes=None):

    #df_mes = pd.DataFrame(list(Mes.objects.all().values()),columns=["id","nombre"])
    df_liquidacion_concepto = pd.DataFrame(list(Concepto.objects.all().filter(ordenliq__isnull=False).values()),columns=["concepto","descrip"])
    df_hliquidac = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=11001005, mes=mes).values()),columns=["concepto_id","mes_id","monto"])
    df_join = df_hliquidac.set_index('concepto_id').join(df_liquidacion_concepto.set_index('concepto')) # Muestra ordenliq =/ NULL
    #df_resul = df_join.set_index('mes_id').join(df_mes.set_index('id')) # Join con tabla meses para mostrar nombre

    print(df_join)

    qs=pd.pivot_table(df_join,index=["descrip"], columns=["mes_id"], values="monto", fill_value=0)


    resul = format_html(qs.to_html())
    return render(request, 'persona/prueba.html', {'resul':resul})
