from django.shortcuts import redirect
from django.http import JsonResponse
from django.db import connection, OperationalError, InternalError
from pymysql import IntegrityError
def crear_tarea(request):
    if request.method == 'POST' and request.is_ajax():
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("TAREA_MANTENIMIENTO", [request.session.get("email"), request.POST.get("nserie"), request.POST.get("equipo"), request.POST.get("fecha"), request.POST.get("sl_usuario"), request.POST.get("tipo_mant"), request.POST.get("estado")])
            mensaje = cursor.fetchall()[0][0]

            return JsonResponse({"status": "success", "msg": mensaje}, status=200)
        except (InterruptedError, InternalError, OperationalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "No se pudo realizar la tarea"}, status=200)
        finally:
            cursor.close()
    else:
        return redirect("mantenimiento")

def modificar_mant(request):
    if request.method == 'POST':
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("ESTADO_MANTENIMIENTO", [request.session.get("email"), request.POST.get("id_mant"), request.POST.get("sl_nuevo_estado")])
            mensaje = cursor.fetchall()[0][0]
            return JsonResponse({"status": "success", "msg": mensaje}, status=200)
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error al actualizar tarea"}, status=200)
        finally:
            cursor.close()
    else:
        return redirect("mantenimiento")