from django.shortcuts import render
from django.utils.html import format_html
from .models import *
import pandas as pd

def liquidaciones(request):
    return render(request, 'persona/prueba.html')

def extra(request, mes=None):
    df = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=11001005, mes=mes).values()),columns=["concepto_id","mes_id","monto"])
    qs=pd.pivot_table(df,index=["concepto_id"], columns=["mes_id"], values="monto", fill_value=0)
    resul = format_html(qs.to_html())
    return render(request, 'persona/prueba.html', {'resul':resul})
