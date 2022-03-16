from django.shortcuts import redirect, render
from django.db import IntegrityError, OperationalError, connection

def vista_graficas(request):
    if request.session.get("email"):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM app_inventario")
            productos = cursor.fetchall()
        except (OperationalError, IntegrityError):
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        context = {
            "productos": productos,
            "privilegio": request.session.get("privilegio"),
        }
        return render(request, "RES/resultados.html", context)
    else:
        return redirect("/cerrar_sesion")