from django.shortcuts import redirect, render
from django.db import connection, IntegrityError, InternalError, OperationalError

def sigssmac_vista(request):
    if request.session.get("email"):
        context = {
            'email': request.session.get("email"),
            'privilegio': request.session.get("privilegio"),
        }
        try:
            cursor = connection.cursor()
            cursor.callproc("SIGSSMAC_REPORTES")
            context["detalles"] = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        return render(request, "sigssmac.html", context)
    else:
        return redirect("/cerrar_sesion")