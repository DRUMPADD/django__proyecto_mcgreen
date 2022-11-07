from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.db import InternalError as errors, IntegrityError as errors, InterfaceError as errors, ProgrammingError as errors
import json

def show_corrective_mant(request):
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.callproc("MOSTRAR_MANTENIMIENTO_CORRECTIVO")
        get_info = cursor.fetchall()
        return JsonResponse({"msg": get_info}, status=200)
    except (errors) as e:
        print(e)
        return JsonResponse({"msg": None}, status=200)

def create_manteinment(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.execute("INSERT INTO mantenimiento_corr (maq_eq_id_fk, novedad_id_fk, fecha_reporte, mod_fallo_fk, fecha_entrega, contador_dias, observaciones) values(%s, %s, %s, %s, %s, %s, %s)", [responses.get("item"), responses.get("novedad"), responses.get("report_date"), responses.get("fail"), responses.get("rec_date"), responses.get("days"), responses.get("notes")])
            return JsonResponse({"status": "success", "msg": "Mantenimiento correctivo agregado"}, status=200)
        except (errors) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def modify_manteinment(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.execute("UPDATE mantenimiento_corr SET maq_eq_id_fk = %s, novedad_id_fk = %s, fecha_reporte = %s, mod_fallo_fk = %s, fecha_entrega = %s, contador_dias = %s, observaciones = %s where id_corr = %s", [responses.get("item"), responses.get("novedad"), responses.get("report_date"), responses.get("fail"), responses.get("rec_date"), responses.get("days"), responses.get("notes"), responses.get("corr_id")])
            return JsonResponse({"status": "success", "msg": "Mantenimiento correctivo actualizado"}, status=200)
        except (errors) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)

def delete_manteinment(request):
    if request.method == 'POST':
        responses = json.loads(request.body.decode("utf-8"))
        try:
            cursor = connections["mcgreen_conexion"].cursor()
            cursor.execute("DELETE FROM mantenimiento_corr WHERE id_corr = %s", [responses.get("corr_id")])
            return JsonResponse({"status": "success", "msg": "Mantenimiento correctivo eliminado"}, status=200)
        except (errors) as e:
            print(e)
            return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)