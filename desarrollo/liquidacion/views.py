from django.shortcuts import render


def prueba(request):
    if request.method == 'POST':
        pass
    return render(request, 'persona/prueba.html')
