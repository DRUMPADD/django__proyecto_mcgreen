from django.http import JsonResponse
from django.db import connections
from django.db import InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError
import json

def showNovelties(request):
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.execute("SELECT * FROM novedad")
        return JsonResponse({"msg": cursor.fetchall()}, status=200)
    except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
        print(e)
        return JsonResponse({"msg": None}, status=200)

def createNovelty(request):
    if request.method == 'POST':
        answers = json.loads(request.body.decode("utf-8"))
        print(answers)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("NOVEDAD_AGREGAR", [answers.get("name")])
            return JsonResponse({"status": "success", "msg": "Tipo de novedad agregada"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def modifyNovelty(request):
    if request.method == 'POST':
        answers = json.loads(request.body.decode("utf-8"))
        print(answers)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("NOVEDAD_MODIFICAR", [answers.get("id"), answers.get("name")])
            return JsonResponse({"status": "success", "msg": "Tipo de novedad: "+ answers.get("id") +" actualizada"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def deleteNovelty(request):
    if request.method == 'POST':
        answers = json.loads(request.body.decode("utf-8"))
        print(answers)
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("NOVEDAD_ELIMINAR", [answers.get("id")])
            return JsonResponse({"status": "success", "msg": "Tipo de novedad: "+ answers.get("id") +" eliminada"}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def searchNovelty(request):
    if request.method == 'POST':
        answers = json.loads(request.body.decode("utf-8"))
        print(answers)
        resp = ""
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.callproc("NOVEDAD_BUSCAR_EXISTENTE", [answers.get("id")])
            resp = cursor.fetchone()[0]
            if resp == "EXISTE":
                return JsonResponse({"status": "success", "msg": resp}, status=200)
            else:
                return JsonResponse({"status": "success", "msg": ""}, status=200)
        except (InternalError, IntegrityError, InterfaceError, ProgrammingError, DataError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)