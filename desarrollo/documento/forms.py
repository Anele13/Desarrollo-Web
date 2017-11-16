from sqlalchemy import create_engine
from django import forms
import csv, operator
from sqlalchemy import create_engine
from sqlalchemy import MetaData

def listar_tablas():
    '''
    Función listar tablas:
    Se encarga de devolver las tablas de la base que se podran cargar posteriormente desde archivos CSV.
    :return: Lista modificada de la base con las tablas disponibles.
    '''
    engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_economia', pool_recycle=3600)
    elementos_a_borrar=['django_session',
                        'django_migrations',
                        'auth_group',
                        'auth_group_permissions',
                        'auth_permission',
                        'django_content_type',
                        'usuario',
                        'django_permission',
                        'django_admin',
                        'persona_usuario_groups',
                        'persona_usuario_user_permissions',
                        'django_admin_log',
                        'documento_documento',
                        'documento_pdf572',
                        'persona_agente',
                        'persona_usuario',
                        'persona_administrador']
    diccionario={}
    for nombre_tabla in engine.table_names():
        if nombre_tabla not in elementos_a_borrar:
            diccionario[nombre_tabla]=nombre_tabla
    return (tuple(diccionario.items()))

class UploadForm(forms.Form):
    '''
    Corresponde a la carga de los archivos CSV.
    '''
    tabla= forms.ChoiceField(widget = forms.Select())
    docfile = forms.FileField(label='Selecciona un archivo')

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields['tabla'] = forms.ChoiceField(choices=listar_tablas())
