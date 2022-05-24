from django.db import connection, OperationalError, IntegrityError, InternalError
from django.http import JsonResponse

def sigssmac_post(request):
    accident = request.POST.get("accidentabilidad")
    ctrl_cambios = request.POST.get("control_cambios")
    info = request.POST.get("informacion")
    hallazgos = request.FILES["hallazgos"]
    print(accident)
    print(ctrl_cambios)
    print(info)
    print(hallazgos)
    try:
        cursor = connection.cursor()
        cursor.callproc("SIGSSMAC", [request.session.get("email"), accident, ctrl_cambios, info, hallazgos, hallazgos.name])
        mensaje = cursor.fetchall()[0][0]
        img_save_path = 'media/img/sigssmac/' + hallazgos.name
        print(img_save_path)
        with open(img_save_path, 'wb+') as f:
            for chunk in hallazgos.chunks():
                f.write(chunk)
        return JsonResponse({"status": "success", "msg": mensaje}, status=200)
    except (OperationalError, IntegrityError, InternalError) as e:
        print(e)
        return JsonResponse({"status": "error", "msg": "Error en el sistema"}, status=200)
    finally:
        cursor.close()