from django.db import models
import pandas as pd
from sqlalchemy import create_engine
import codecs

class Documento(models.Model):
 filename = models.CharField(max_length=100)
 docfile = models.FileField(upload_to='csv/')

 def csv_to_base(self,documento):
     engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_economia')
     filer= codecs.open(documento.docfile.path, "r+",encoding='utf-8', errors='ignore')
     archivocsv=pd.DataFrame.from_csv(filer, sep=',')
     if documento.filename != 'liquidacion_hliquidac':
         engine.execute("DELETE FROM "+documento.filename)
         #no se borra en hlquidac por el tamaño de los registros(7m)
         #se apendea con la totaliad de la confianza que viene en el csv
     archivocsv.to_sql(documento.filename, engine, if_exists='append', schema='public')
     filer.close()
