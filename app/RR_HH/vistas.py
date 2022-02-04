from django.shortcuts import redirect, render


def directorio(request):
    if request.session.get("email"):
        context = {
            'privilegio': request.session.get("privilegio")
        }
        return render(request, 'RRHH/directorio.html', context)
    else:
        return redirect("/cerrar_sesion")

def perfil_puesto(request):
    if request.session.get("email"):
        context = {
            'privilegio': request.session.get("privilegio")
        }
        return render(request, 'RRHH/perfil_puesto.html', context)
    else:
        return redirect("/cerrar_sesion")