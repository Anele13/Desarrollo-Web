from django.db import models
import pandas
from sqlalchemy import create_engine

class Documento(models.Model):
 filename = models.CharField(max_length=100)
 docfile = models.FileField(upload_to='csv/')

 def reemplazar_comillas(self,doc):
     char1 = chr(34)
     char2 = ' '

     filer = open(doc.docfile.path, "r")
     filew = open(doc.docfile.path+'.txt', "w")

     buff = filer.read()
     rbuff = buff.replace(char1, char2)

     filew.write(rbuff)

     filer.close()
     filew.close()


 def csv_to_base(self,documento):
     self.reemplazar_comillas(documento)
     engine = create_engine('postgresql://postgres:holamundo@localhost:5432/db_economia')
     archivocsv=pandas.DataFrame.from_csv(documento.docfile.path, sep=',')
     engine.execute("DELETE FROM "+documento.filename)
     archivocsv.to_sql(documento.filename, engine, if_exists='append', schema='public')
