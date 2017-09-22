from django.db import models
import pandas
from sqlalchemy import create_engine

class Documento(models.Model):
 filename = models.CharField(max_length=100)
 docfile = models.FileField(upload_to='csv/')

 def csv_to_base(self,documento):
     engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_economia')
     archivocsv=pandas.DataFrame.from_csv(documento.docfile.path, sep=',')
     engine.execute("DELETE FROM "+documento.filename)
     archivocsv.to_sql(documento.filename, engine, if_exists='append', schema='public')
