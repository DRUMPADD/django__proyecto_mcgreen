from django.shortcuts import render
from django.db import connection, IntegrityError, InternalError, OperationalError

def sigssmac_vista(request):
    context = {}
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