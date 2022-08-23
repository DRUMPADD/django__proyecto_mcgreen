from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import InterfaceError, InternalError, OperationalError, ProgrammingError, connection

def accidentabilidad_vista(request):
    if request.session.get("email"):
        context = {
            "saludo": "Accidentabilidad",
            'email': request.session.get("email"),
            'privilegio': request.session.get("privilegio"),
        }
        try:
            cursor = connection.cursor()
            cursor.execute("select * from app_personal_propio")
            context["personal_propio"] = cursor.fetchall()
        except (OperationalError, InterfaceError, ProgrammingError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        try:
            cursor = connection.cursor()
            cursor.execute("select * from app_personal_con")
            context["personal_contratado"] = cursor.fetchall()
        except (OperationalError, InterfaceError, ProgrammingError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        try:
            cursor = connection.cursor()
            cursor.callproc("DETALLES_ACCIDENTABILIDAD")
            estadisticas = cursor.fetchall()
            context["detalles_acci"] = estadisticas
            cont_total_acc = 0
            cont_emp = 0
            for est in estadisticas:
                cont_total_acc = cont_total_acc + est[4]
                cont_emp = cont_emp + est[1]
            context["total_est"] = cont_total_acc
            context["total_emp"] = cont_emp
        except (OperationalError, InterfaceError, ProgrammingError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        return render(request, "RRHH/accidentabilidad.html", context)
    else:
        return redirect("/cerrar_sesion")


def datos_x_meses(request):
    mensaje = ""
    try:
        cursor = connection.cursor()
        cursor.callproc("DETALLES_ACCIDENTABILIDAD")
        mensaje = cursor.fetchall()
        print(mensaje)
        for con in mensaje:
            print(con)
        return JsonResponse({"respuesta": mensaje}, status=200) 
    except (OperationalError, InternalError, ProgrammingError) as e:
        print(e)
        return JsonResponse({"respuesta": "Error en el sistema"}, status=200)