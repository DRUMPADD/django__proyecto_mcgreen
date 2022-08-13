from django.http import JsonResponse
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
    try:
        cursor = connection.cursor()
        cursor.callproc("DETALLES_ACCIDENTABILIDAD")
        context["detalles_acci"] = cursor.fetchall()
    except (OperationalError, InterfaceError, ProgrammingError) as e:
        print(e)
        return render(request, "errors/error500.html", {
            "mensaje": "Contacte con el servicio de sistemas"
        })
    return render(request, "RRHH/accidentabilidad.html", context)



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

def accidentabilidad_res_totales(request):
    mensaje = ""
    try:
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        cursor.execute("select mes_subcon, sum(cant_con_p), sum(total_calculo) from app_personal_con group by mes_subcon")
        cursor2.execute("select mes_propio, sum(cant_pro_p), sum(total_calculo) from app_personal_propio group by mes_propio")
        mensaje = cursor.fetchall()
        mensaje2 = cursor2.fetchall()
        
        print(mensaje)
        print(mensaje2)
        for pro in mensaje:
            print(pro)
        return JsonResponse({"propios": mensaje}, status=200) 
    except (OperationalError, InternalError, ProgrammingError) as e:
        print(e)