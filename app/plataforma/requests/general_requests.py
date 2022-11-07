from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.db import InternalError, IntegrityError, InterfaceError, ProgrammingError
import json


def show_general_mant(request):
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.callproc("MOSTRAR_MANTENIMIENTO_PREVENTIVO")
        get_info = cursor.fetchall()
        return JsonResponse({"msg": get_info}, status=200)
    except (InternalError, IntegrityError, InterfaceError, ProgrammingError) as e:
        print(e)
        return JsonResponse({"msg": "Error en el sistema"}, status=200)
    except ValueError as e:
        return HttpResponse("<h1>Nada</h1>")
    finally:
        cursor.close()


def create_general(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        print(responses)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("MANTENIMIENTO_PREV_AGREGAR", [responses.get("item_id"), responses.get("frec_"), responses.get("create_date"), responses.get("act_"), responses.get("date_next")])
            return JsonResponse({"status": "success", "msg": "Mantenimiento preventivo agregado"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def modify_general(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        print(responses)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("MANTENIMIENTO_PREV_MODIFICAR", [responses.get("item_id"), responses.get("frec_"), responses.get("create_date"), responses.get("act_"), responses.get("date_next"), responses.get("prev_cod")])
            return JsonResponse({"status": "success", "msg": "Mantenimiento preventivo actualizado"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def delete_general(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        print(responses)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("MANTENIMIENTO_PREV_ELIMINAR", [responses.get("prev_id")])
            return JsonResponse({"status": "success", "msg": "Mantenimiento preventivo eliminado"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
