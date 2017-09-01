from django.shortcuts import render
from django.utils.html import format_html
from .models import *

import pandas as pd

def nada():
    pass

def prueba(request):

    df = pd.DataFrame(list(Hliquidac.objects.all().filter(documento=11001005).values()),columns=["concepto_id","mes_id","monto"])

    #qs = pd.crosstab(df["concepto_id"], df["mes_id"],margins=True)
    #qs=pd.pivot_table(df,index=["concepto_id", "monto"], columns=["mes_id"], fill_value=0)

    qs=pd.pivot_table(df,index=["concepto_id"], columns=["mes_id"], values="monto", fill_value=0)
    resul = format_html(qs.to_html())
    return render(request, 'persona/prueba.html', {'resul':resul})
