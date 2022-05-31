from django.db import connection, OperationalError, IntegrityError, InternalError
from django.http import JsonResponse

def sigssmac_post(request):
    fecha_inicio = request.POST.get("fecha_inicio")
    fecha_compromiso = request.POST.get("fecha_compromiso")
    fecha_cierre = request.POST.get("fecha_cierre")
    indice_actos = request.POST.get("indice_actos")
    origen = request.POST.get("sl_origen")
    herramientas = request.POST.get("herramientas") if request.POST.get("herramientas") != None else 'N/A'
    tipo_i = request.POST.get("sl_tipo_i")
    acto = request.POST.get("sl_acto")
    afecta = request.POST.get("sl_afecta") if request.POST.get("sl_afecta") != None or request.POST.get("sl_afecta") != '' else 'N/A'
    categoria = request.POST.get("categoria")
    hallazgo_obser = request.POST.get("hallazgo_obser")
    accion = request.POST.get("accion")
    responsable = request.POST.get("sl_responsable")
    prioridad = request.POST.get("sl_prioridad")
    estatus = request.POST.get("sl_status")
    hallazgos = request.FILES["hallazgos"]
    
    print(fecha_inicio)
    print(fecha_compromiso)
    print(fecha_cierre)
    print(indice_actos)
    print(origen)
    print(herramientas)
    print(tipo_i)
    print(acto)
    print(afecta)
    print(categoria)
    print(hallazgo_obser)
    print(accion)
    print(responsable)
    print(prioridad)
    print(estatus)

    try:
        cursor = connection.cursor()
        cursor.callproc("SIGSSMAC", [request.session.get("email"), fecha_inicio, herramientas, origen, tipo_i, acto, afecta, categoria, hallazgo_obser, accion, indice_actos, responsable, prioridad, estatus, fecha_compromiso, fecha_cierre, hallazgos, hallazgos.name])
        mensaje = cursor.fetchall()[0][0]
        img_save_path = 'media/img/sigssmac/' + hallazgos.name
        print(img_save_path)
        if mensaje == 'Datos almacenados en el sistema':
            with open(img_save_path, 'wb+') as f:
                for chunk in hallazgos.chunks():
                    f.write(chunk)
            return JsonResponse({"status": "success", "msg": mensaje}, status=200)
        else:
            return JsonResponse({"status": "error", "msg": mensaje}, status=200)
    except (OperationalError, IntegrityError, InternalError) as e:
        print(e)
        return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
    finally:
        cursor.close()