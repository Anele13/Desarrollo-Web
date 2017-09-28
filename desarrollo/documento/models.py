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
     archivocsv=pd.DataFrame.from_csv(filer, sep=';')
     engine.execute("DELETE FROM "+documento.filename)
     archivocsv.to_sql(documento.filename, engine, if_exists='append', schema='public')
     filer.close()
