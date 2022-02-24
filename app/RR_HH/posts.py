from django.db import IntegrityError, OperationalError, connection
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from easy_pdf.rendering import render_to_pdf_response

def crear_perfil(request):
    if request.method == 'POST' and request.is_ajax():
        print("Perfil")
        mensaje_salida = ""
        mensaje = ""
        mensaje_error = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("AGREGAR_PUESTO", [request.POST["email_usuario"], request.POST["puesto"], "Hola", request.POST["sl_departamentos"], request.POST["empresa"], request.POST["obj_puesto"], request.POST["vacantes"]])
            mensaje = cursor.fetchall()[0][0]
            mensaje_salida = "Perfil de puesto creado!!"
        except:
            mensaje_error = "Error al crear el puesto"
        finally:
            cursor.close()
        return JsonResponse({"msg": mensaje, "msg_salida": mensaje_salida, "msg_error": mensaje_error, "puesto_creado": ""}, status=200)

def crear_directorio(request):
    if request.method == 'POST' and request.is_ajax():
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("AGREGAR_EMPLEADO_V2", [request.session.get("email"), "", request.POST.get("nombre_emp"), request.POST.get("ap_paterno"), request.POST.get("ap_materno"), request.POST.get("sl_puesto"),request.POST.get("fecha_registro"), request.POST.get("edad"), request.POST.get("grado_estudio"), request.POST.get("direccion"), request.POST.get("sl_sexo"), request.POST.get("estado"), request.POST.get("tipo_sangre"), request.POST.get("cont_emergencia"), request.POST.get("emergencia"), request.POST.get("experiencia"), request.POST.get("cap_requerida"), request.POST.get("nss"), request.POST.get("curp"), request.POST.get("rfc"), request.POST.get("correo"), request.POST.get("celular")])
            mensaje = cursor.fetchall()[0][0]
        except OperationalError as oe:
            return HttpResponse(oe, status=500)
        except IntegrityError as ie:
            return HttpResponse(ie.message, status=500)
        finally:
            cursor.close()
        if mensaje == 'CARACTERISTICAS AGREGADAS A EL EMPLEADO':
            return JsonResponse({"bg_msg": "Datos enviados","msg": mensaje, "state": "success"}, status=200)
        else:
            return JsonResponse({"bg_msg": "Error ocurrido", "msg": mensaje, "state": "error"}, status=500)

def mostrar_perfil_url(request, nombre_perfil=""):
    if request.session.get("email"):
        if nombre_perfil != "":
            sup = connection.cursor()
            sup.callproc("MOSTRAR_PUESTOS_V2_SUPERVISAR", [nombre_perfil])
            supervisar = sup.fetchall()
            sup.close()
            
            supviso = connection.cursor()
            supviso.callproc("MOSTRAR_PUESTOS_V2_TSUPERVISAN", [nombre_perfil])
            superviso = supviso.fetchall()
            supviso.close()
            
            pe = connection.cursor()
            pe.callproc("MOSTRAR_PUESTOS_V2", [nombre_perfil])
            mas_info = pe.fetchall()
            pe.close()
            pe1 = connection.cursor()
            pe1.callproc("MOSTRAR_PUESTOS_V2_P1", [nombre_perfil])
            mas_info1 = pe1.fetchall()
            pe1.close()
            pe2 = connection.cursor()
            pe2.callproc("MOSTRAR_PUESTOS_V2_P2", [nombre_perfil])
            mas_info2 = pe2.fetchall()
            pe2.close()
            pe3 = connection.cursor()
            pe3.callproc("MOSTRAR_PUESTOS_V2_P3", [nombre_perfil])
            mas_info3 = pe3.fetchall()
            pe3.close()
            pe4 = connection.cursor()
            pe4.callproc("MOSTRAR_PUESTOS_V2_P4", [nombre_perfil])
            mas_info4 = pe4.fetchall()
            pe4.close()
            pe5 = connection.cursor()
            pe5.callproc("MOSTRAR_PUESTOS_V2_P5", [nombre_perfil])
            mas_info5 = pe5.fetchall()
            pe5.close()
            pe6 = connection.cursor()
            pe6.callproc("MOSTRAR_PUESTOS_V2_P6", [nombre_perfil])
            mas_info6 = pe6.fetchall()
            pe6.close()
            pe7 = connection.cursor()
            pe7.callproc("MOSTRAR_PUESTOS_V2_P7", [nombre_perfil])
            mas_info7 = pe7.fetchall()
            pe7.close()
            context = {
                'pagesize': 'A4',
                "titulo": "Fluidos McGreen ",
                "nombre_perfil": nombre_perfil,
                "mas_info": mas_info,
                "supervisar": supervisar,
                "superviso": superviso,
                "mas_info1": mas_info1,
                "mas_info2": mas_info2,
                "mas_info3": mas_info3,
                "mas_info4": mas_info4,
                "mas_info5": mas_info5,
                "mas_info6": mas_info6,
                "mas_info7": mas_info7,
            }
            return render_to_pdf_response(request, 'ver_perfil.html', context)
        else:
            return redirect("perfil_y_directorio")
    else:
        return redirect("/cerrar_sesion")