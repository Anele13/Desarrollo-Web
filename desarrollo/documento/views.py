from django.shortcuts import render
from documento.forms import UploadForm
from documento.models import Documento
from django.shortcuts import render, redirect
import os

# Create your views here.
def subir_archivo(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Documento(filename = request.POST['filename'],docfile = request.FILES['docfile'])
            newdoc.save()
            newdoc.csv_to_base(newdoc)
            newdoc.delete()
            if os.path.isfile(newdoc.docfile.path):
                os.remove(newdoc.docfile.path)
            return redirect("uploads")
    else:
        form = UploadForm()
    return render(request, 'documento/upload.html', {'form': form})
