from django.http import JsonResponse
from django.db import connections
from django.db import InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError
import json

def showModes(request):
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.execute("SELECT * FROM modos_fallo")
        return JsonResponse({"msg": cursor.fetchall()}, status=200)
    except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
        print(e)
        return JsonResponse({"msg": None}, status=200)

def createMode(request):
    if request.method == 'POST':
        answers = json.loads(request.body.decode("utf-8"))
        print(answers)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("MODOS_AGREGAR", [answers.get("id"), answers.get("name")])
            return JsonResponse({"status": "success", "msg": "Modo de fallo agregado"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def modifyMode(request):
    if request.method == 'POST':
        answers = json.loads(request.body.decode("utf-8"))
        print(answers)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("MODOS_MODIFICAR", [answers.get("id"), answers.get("name")])
            return JsonResponse({"status": "success", "msg": "Modo de fallo: "+ answers.get("id") +" actualizado"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def deleteMode(request):
    if request.method == 'POST':
        answers = json.loads(request.body.decode("utf-8"))
        print(answers)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("MODOS_ELIMINAR", [answers.get("id")])
            return JsonResponse({"status": "success", "msg": "Modo de fallo: "+ answers.get("id") +" eliminado"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def searchMode(request):
    if request.method == 'POST':
        answers = json.loads(request.body.decode("utf-8"))
        print(answers)
        resp = ""
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("MODOS_BUSCAR_EXISTENTE", [answers.get("id")])
            resp = cursor.fetchone()[0]
            if resp == "EXISTE":
                return JsonResponse({"status": "success", "msg": resp}, status=200)
            else:
                return JsonResponse({"status": "success", "msg": ""}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
