from django.db import models
import pandas as pd
from sqlalchemy import create_engine
import codecs

class Documento(models.Model):
 filename = models.CharField(max_length=100)
 docfile = models.FileField(upload_to='csv/')

 def csv_to_base(self,documento):
     engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_economia')
     filer= codecs.open(documento.docfile.path, "r+",encoding='latin-1')
     #archivocsv=pd.DataFrame.from_csv(filer, sep=';')
     archivocsv=pd.read_csv(filer, sep=',',dtype=object)
     archivocsv.set_index(archivocsv.columns[1],inplace=True)

     if documento.filename != 'liquidacion_hliquidac':
         engine.execute("DELETE FROM "+documento.filename)
         #no se borra en hlquidac por el tamaño de los registros(7m)
         #se apendea con la totaliad de la confianza que viene en el csv
     archivocsv.to_sql(documento.filename, engine, if_exists='append', schema='public')
     filer.close()


class Pdf572(models.Model):
    cuil = models.BigIntegerField()
    periodo = models.IntegerField()
    presentacion = models.IntegerField()
    docfile = models.FileField(upload_to='formulario_f572/')
    tipo =  models.CharField(max_length=3)
