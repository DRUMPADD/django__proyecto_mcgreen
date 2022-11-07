from django.http import JsonResponse
from django.db import connections
from django.db import InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, DatabaseError, OperationalError
import json

def show_items(request):
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.callproc("EQUIPOS_MOSTRAR")
        items = cursor.fetchall()
        print(items)
        return JsonResponse({"msg": items}, status=200)
    except (ProgrammingError, InternalError, InterfaceError, IntegrityError) as e:
        print(e)
        return JsonResponse({"msg": None}, status=200)

def create_item(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        print(responses.get("cod_"))
        print(responses.get("name_"))
        print(responses.get("quantity"))
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("EQUIPO_AGREGAR", [responses.get("cod_"), responses.get("name_"), responses.get("quantity")])
            confirm_message = cursor.fetchall()
            print(confirm_message)
            if not confirm_message:
                return JsonResponse({"status": "success", "msg": "Item agregado"}, status=200)
            else:
                return JsonResponse({"status": "error", "msg": confirm_message[0][0]}, status=200)
        except (ProgrammingError, InternalError, InterfaceError, IntegrityError, DataError, DatabaseError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def modify_item(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        print(responses.get("id_"))
        print(responses.get("new_name"))
        print(responses.get("new_stuck"))
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("EQUIPO_MODIFICAR", [responses.get("new_name"), responses.get("new_stuck"), responses.get("id_")])
            return JsonResponse({"status": "success", "msg": "Item actualizado"}, status=200)
        except (ProgrammingError, InternalError, InterfaceError, IntegrityError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
        finally:
            cursor.close()

def delete_item(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode("utf-8"))
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("ELIMINAR_ITEM", [response.get("cod_item")])
            return JsonResponse({"status": "success", "msg": "Equipo eliminado"}, status=200)
        except (ProgrammingError, InternalError, InterfaceError, IntegrityError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
        finally:
            cursor.close()

def delete_item_complete(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode("utf-8"))
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("ELIMINAR_ITEM_COMPLETO", [response.get("cod_item")])
            return JsonResponse({"status": "success", "msg": "Equipo eliminado por completo"}, status=200)
        except (ProgrammingError, InternalError, InterfaceError, IntegrityError) as e:
            print(e)
            return JsonResponse({"msg": "Error en el sistema"}, status=200)

def search_item(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode("utf-8"))
        print("Respuesta:",response.get("cod_item"))
        found_ = ""
        found_2 = ""
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("BUSCAR_ITEM_EN_MANTENIMIENTO_PREVENTIVO", [response.get("cod_item")])
            found_ = cursor.fetchall()
            print(found_)
        except (ProgrammingError, InternalError, InterfaceError, IntegrityError) as e:
            print("Error:",e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
        finally:
            cursor.close()
        try:
            cursor2 = connections["mcgreen_conexion"].cursor()
            cursor2.callproc("BUSCAR_ITEM_EN_MANTENIMIENTO_CORRECTIVO", [response.get("cod_item")])
            found_2 = cursor2.fetchall()
            print(found_2)
        except (ProgrammingError, InternalError, InterfaceError, IntegrityError) as e:
            print("Error:",e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
        finally:
            cursor2.close()
        
        if found_ and found_2:
            return JsonResponse({"status": "success", "msg": "Encontrados"}, status=200)
        elif found_ or found_2:
            return JsonResponse({"status": "success", "msg": "Encontrado"}, status=200)
        else:
            return JsonResponse({"status": "success", "msg": "No encontrado"}, status=200)

def modify_carateristics(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("MODIFICAR_CARACTERISTICAS", [responses.get("item_id"), responses.get("name_"), responses.get("quantity"), responses.get("brand"), responses.get("bought_date"), responses.get("state"), responses.get("model"), responses.get("serial_n"), responses.get("location"), responses.get("date_")])
            return JsonResponse({"status": "success", "msg": "Características agregadas"}, status=200)
        except (ProgrammingError, InternalError, InterfaceError, IntegrityError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

# Copiar archivo