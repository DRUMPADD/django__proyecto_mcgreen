from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import InterfaceError, InternalError, OperationalError, ProgrammingError, connection

def accidentabilidad_vista(request):
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
    return render(request, "RRHH/accidentabilidad.html", context)



def accidentabilidad_contratados(request):
    mensaje = ""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT total_calculo FROM app_personal_con")
        mensaje = cursor.fetchall()
        print(mensaje)
        return JsonResponse({"contratados": mensaje}, status=200) 
    except (OperationalError, InternalError, ProgrammingError) as e:
        print(e)
def accidentabilidad_propios(request):
    mensaje = ""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT total_calculo FROM app_personal_con")
        mensaje = cursor.fetchall()
        print(mensaje)
        return JsonResponse({"propios": mensaje}, status=200) 
    except (OperationalError, InternalError, ProgrammingError) as e:
        print(e)