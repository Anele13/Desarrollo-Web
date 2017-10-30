"""desarrollo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from persona import views as pviews
from liquidacion import views as lviews
from documento import views as dviews


urlpatterns = [
    url(r'^$', pviews.home, name='home'),
    url(r'^login/$', pviews.login_usuario, name='login'),
    url(r'^home/$', pviews.home, name='home'),
    url(r'^nuevo_usuario/$', pviews.nuevo_usuario, name='nuevo_usuario'),
    url(r'^logout/$',pviews.salir, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^agente/$', pviews.mostrar_agente, name= 'mostrar_agente'),
    url(r'^administrador/$', pviews.mostrar_administrador, name= 'mostrar_administrador'),
    url(r'^liquidacion/$', lviews.liquidaciones, name= 'liquidaciones_agente'),
    url(r'^liquidacion/(?P<mes>[0-9]+)/$', lviews.liquidaciones, name= 'liquidaciones_agente'),
    url(r'^liquidacion/(?P<documento>[0-9]+)/(?P<mes>[0-9]+)$', lviews.liquidaciones, name= 'liquidaciones_agente'),
    url(r'^liquidacion/(?P<documento>[0-9]+)$', lviews.liquidaciones, name= 'liquidaciones_agente'),
    url(r'^liqPDF/(?P<documento>[0-9]+)/(?P<mes>[0-9]+)$', lviews.PdfLiquidacion.as_view(), name= 'liquidaciones_a_pdf'),
    url(r'^liqPDF/(?P<documento>[0-9]+)$', lviews.PdfLiquidacion.as_view(), name= 'liquidaciones_a_pdf'),
    url(r'^liqPDF/$', lviews.PdfLiquidacion.as_view(), name= 'liquidaciones_a_pdf'),
    url(r'^agentes-a-cargo/$', pviews.agentes_a_cargo, name= 'agentes_a_cargo'),
    url(r'^reportes-agentes/$', pviews.reportes_agentes, name= 'reportes_agentes'),
    url(r'^f572/$', dviews.presentacion_f572, name= 'presentacion_f572'),
    url(r'^pdf_572/(?P<cuil>[\w-]+)$', dviews.pdf_form572, name= 'pdf_572'),


    #super administrador
    url(r'^uploads/$', dviews.mostrar_super_admin, name="mostrar_super_admin"),
    url(r'^archivo/$', dviews.subir_archivo, name="carga_csv"),
    url(r'^alta/$', dviews.alta_admin, name="alta_empresa_admin"),

    #cambiar contraseña
    url(r'^password/$', pviews.cambiar_contraseña, name='cambiar_contraseña'),
]
