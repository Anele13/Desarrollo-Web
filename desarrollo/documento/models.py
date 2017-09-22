from django.db import models
import pandas
from sqlalchemy import create_engine

class Documento(models.Model):
 filename = models.CharField(max_length=100)
 docfile = models.FileField(upload_to='csv/')

 def csv_to_base(self,documento):
     RUTA_CSV=documento.docfile.path
     engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_economia')
     archivocsv=pandas.DataFrame.from_csv(RUTA_CSV, sep=',')
     archivocsv.to_sql(documento.filename, engine, if_exists='append', schema='public')
