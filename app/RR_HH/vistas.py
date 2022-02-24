from audioop import reverse
from django.shortcuts import redirect, render
from django.db import OperationalError, connection

def directorio_perfil(request):
    if request.session.get("email"):
        try:
            cursor = connection.cursor()
            puestos = connection.cursor()
            puestos = cursor.execute("SELECT * from app_puestos")
            puestos = cursor.fetchall()
        except OperationalError as oe:
            print("Error de operación en la base")
            return False
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            departamentos = connection.cursor()
            departamentos = cursor.execute("SELECT * from app_departamento")
            departamentos = cursor.fetchall()
        except OperationalError as oe:
            print("Error de operación en la base")
            return False
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            empleados = connection.cursor()
            empleados = cursor.execute("SELECT * from app_empleados")
            empleados = cursor.fetchall()
        except OperationalError as oe:
            print("Error de operación en la base")
            return False
        finally:
            cursor.close()
        context = {
            'privilegio': request.session.get("privilegio"),
            'puestos': puestos,
            'departamentos': departamentos,
            'empleados': empleados,
        }
        return render(request, 'RRHH/directorio_perfil.html', context)
    else:
        return redirect(reverse("/cerrar_sesion"))