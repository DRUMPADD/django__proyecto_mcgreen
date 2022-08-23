from django.http import JsonResponse
from django.db import InternalError, OperationalError, ProgrammingError, connection
import json

def accidentabilidad_post(request):
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("ACCIDENTABILIDAD", [request.session.get("email"), res["c_personal"][0], res["h_trabajo"][0], res["jornada"][0], res["c_personal"][1], res["h_trabajo"][1], res["jornada"][1], res["mes"], res["anio"], res["acci_c_baja"][0], res["acci_c_baja"][1], res["dias_inc"][0], res["dias_inc"][1]])
            mensaje = cursor.fetchall()[0]

            return JsonResponse({"status": "success", "res": mensaje}, status=200)
        except (OperationalError, InternalError, ProgrammingError) as e:
            print(e)
            return JsonResponse({"status": "error", "res": "Ocurrió un error en el sistema"}, status=200)