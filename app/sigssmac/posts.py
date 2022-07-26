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
    hallazgos = request.FILES.get("hallazgos")
    
    print(fecha_inicio)
    print(fecha_compromiso)
    print(fecha_cierre)
    print(indice_actos if indice_actos != '' or indice_actos != None else 0)
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
    print(hallazgos if hallazgos != None else '')
    print(hallazgos.name if hallazgos != None else '')
    print(hallazgos.file if hallazgos != None else '')
    
    try:
        cursor = connection.cursor()
        cursor.callproc("SIGSSMAC", [request.session.get("email"), fecha_inicio, herramientas, origen, tipo_i, acto, afecta, categoria, hallazgo_obser, accion, indice_actos, responsable, prioridad, estatus, fecha_compromiso, fecha_cierre, hallazgos.name if hallazgos != None else '', hallazgos.file if hallazgos != None else ''])
        mensaje = cursor.fetchall()[0][0]
        if hallazgos != None:
            img_save_path = 'media/img/sigssmac/' + hallazgos.name
            print(img_save_path)
            with open(img_save_path, 'wb+') as f:
                for chunk in hallazgos.chunks():
                    f.write(chunk)
        if  mensaje == 'Datos almacenados en el sistema':
            return JsonResponse({"status": "success", "msg": mensaje}, status=200)
        else:
            return JsonResponse({"status": "error", "msg": mensaje}, status=200)
    except (OperationalError, IntegrityError, InternalError) as e:
        print(e)
        return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
    finally:
        cursor.close()

def subir_evidencia_despues(request):
    id_sigssmac = request.POST.get("sigss_id")
    evidencia_despues = request.FILES["evidencia_despues"]
    mensaje = ""
    print(id_sigssmac)
    print(evidencia_despues)
    print(evidencia_despues.name)
    try:
        cursor = connection.cursor()
        cursor.callproc("SIGSSMAC_EV_DES", [request.session.get("email"), id_sigssmac, evidencia_despues.name, evidencia_despues])
        mensaje = cursor.fetchall()[0][0]
        print(mensaje)
        img_save_path = 'media/img/sigssmac/' + evidencia_despues.name
        if mensaje == 'Evidencia registrada':
            print(img_save_path)
            with open(img_save_path, 'wb+') as f:
                for chunk in evidencia_despues.chunks():
                    f.write(chunk)
            return JsonResponse({"status": "success", "msg": mensaje}, status=200)
        else:
            return JsonResponse({"status": "error", "msg": mensaje}, status=200)
    except (OperationalError, IntegrityError, InternalError) as e:
        print(e)
        return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
    finally:
        cursor.close()


def agregar_cliente_sigssmac(request):
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            cursor.callproc("Agrega_CLIENTE",[request.session.get("email"), request.POST.get("RFC"), request.POST.get("proveedor"), request.POST.get("direccion"), request.POST.get("telefono"), request.POST.get("email"), "P-SIGSSMAC"])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
            if mensaje == 'Cliente insertado correctamente':
                return JsonResponse({"status": "success", "msg_salida": mensaje}, status=200)
            else:
                return JsonResponse({"status": "error", "msg_salida": mensaje}, status=200)
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return JsonResponse({"status": "error", "msg_salida": "Error en el sistema"}, status=200)
        finally:
            cursor.close()