from django.shortcuts import render


def directorio(request):
    return render(request, 'RRHH/directorio.html')

def perfil_puesto(request):
    return render(request, 'RRHH/perfil_puesto.html')