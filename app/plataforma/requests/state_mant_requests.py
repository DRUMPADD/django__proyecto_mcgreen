from django.http import JsonResponse
from django.db import connections
from django.db import InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError
import json

def showStates(request):
    try:
        getStates = connections["mcgreen_conexion"].cursor()
        getStates.execute("SELECT * FROM estado_plat")
        return JsonResponse({ "msg": getStates.fetchall() }, status=200)
    except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
        print(e)
        return JsonResponse({ "msg": None }, status=200)

def createState(request):
    if request.method == "POST":
        responses = json.loads(request.body.decode("utf-8"))
        print(responses.get("name"))
        try:
            conn = connections["mcgreen_conexion"].cursor()
            conn.callproc("ESTADO_AGREGAR", [responses.get("name")])
            return JsonResponse({ "status": "success", "msg": "Estado agregado" }, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({ "status": "success", "msg": "Error en el sistema" }, status=200)

def modifyState(request):
    if request.method == "POST":
        responses = json.loads(request.body.decode("utf-8"))
        print(responses.get("id"))
        print(responses.get("name"))
        try:
            conn = connections["mcgreen_conexion"].cursor()
            conn.callproc("ESTADO_MODIFICAR", [responses.get("id"), responses.get("name")])
            return JsonResponse({ "status": "success", "msg": "Estado "+ responses.get("id") +" modificado" }, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({ "status": "success", "msg": "Error en el sistema" }, status=200)

def deleteState(request):
    if request.method == "POST":
        responses = json.loads(request.body.decode("utf-8"))
        print(responses.get("id"))
        try:
            conn = connections["mcgreen_conexion"].cursor()
            conn.callproc("ESTADO_ELIMINAR", [responses.get("id")])
            return JsonResponse({ "status": "success", "msg": "Estado "+ responses.get("id") +" eliminado" }, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({ "status": "success", "msg": "Error en el sistema" }, status=200)

def searchState(request):
    if request.method == "POST":
        responses = json.loads(request.body.decode("utf-8"))
        print(responses.get("id"))
        try:
            conn = connections["mcgreen_conexion"].cursor()
            conn.callproc("ESTADO_BUSCAR_EXISTENTE", [responses.get("id")])
            return JsonResponse({ "status": "success", "msg": "Estado "+ responses.get("id") +" eliminado" }, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({ "status": "success", "msg": "Error en el sistema" }, status=200)