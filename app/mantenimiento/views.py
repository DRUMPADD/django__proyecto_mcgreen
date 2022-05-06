from django.shortcuts import redirect, render
from django.db import connection, OperationalError, IntegrityError

def vista_mantenimiento(request):
    if request.session.get("email"):
        context = {}
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_USUARIOS")
            context["usuarios"] = cursor.fetchall()
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_MANTENIMIENTO")
            context["mantenimiento"] = cursor.fetchall()
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
        finally:
            cursor.close()
        return render(request, "Mantenimiento/index_mant.html", context)
    else:
        return redirect("/cerrar_sesion")