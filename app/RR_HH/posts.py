from django.db import IntegrityError, OperationalError, connection
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

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
            print(mensaje)
            mensaje_salida = "Perfil de puesto creado!!"
        except OperationalError:
            mensaje_error = "Error al crear el puesto"
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            mensaje_error = "Error al crear el puesto"
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        return JsonResponse({"msg": mensaje, "msg_salida": mensaje_salida, "msg_error": mensaje_error, "puesto_creado": ""}, status=200)

def funcion1(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        subor = request.POST.get("subordinacion")
        superv = request.POST.get("supervision")
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor2 = connection.cursor()
            if subor != None and superv == None:
                cursor.callproc("AGREGAR_SUB_SUP", ["erick@sigssmac.com.mx", puesto, subor])
                mensaje = cursor.fetchall()[0][0]
                cursor.close()
                print(mensaje)
            elif subor == None and superv != None:
                cursor2.callproc("AGREGAR_SUP", ["erick@sigssmac.com.mx", superv, puesto])
                mensaje = cursor2.fetchall()[0][0]
                cursor2.close()
                print(mensaje)
            else:
                cursor.callproc("AGREGAR_SUB_SUP", ["erick@sigssmac.com.mx", puesto, subor])
                mensaje = cursor.fetchall()[0][0]
                cursor.close()
                cursor2.callproc("AGREGAR_SUP", ["erick@sigssmac.com.mx", superv, puesto])
                cursor2.close()
                print(mensaje)
            cursor.close()
            cursor2.close()
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        if mensaje == "RELACION DE JERARQUIA CREADA":
            return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
        else:
            return JsonResponse({"msg": mensaje, "tipo_res": "error"}, status=500)

def funcion2(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        forma = request.POST.get("formacion")
        escol = request.POST.get("escolaridad")
        per_prof = request.POST.get("per_prof")
        exper = request.POST.get("exper")
        try:
            cursor = connection.cursor()
            cursor.callproc("RH_AGREGAR_PA_PR", ["erick@sigssmac.com.mx", puesto, forma, escol, per_prof, exper])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()

        if mensaje == "PERFIL ACADEMICO Y/O PROFESIONAL AGREGADO CORRECTAMENTE":
            return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
        else:
            return JsonResponse({"msg": mensaje, "tipo_res": "error"}, status=500)

def funcion3(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        funci = request.POST.get("funcion")
        descrip_fun = request.POST.get("descrip_fun")
        perio = request.POST.get("perio")
        try:
            cursor = connection.cursor()
            cursor.callproc("RH_AGREGAR_FUNCION", ["erick@sigssmac.com.mx", puesto, funci, descrip_fun, perio])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == "FUNCION AGREGADA CORRECTAMENTE":
            return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
        else:
            return JsonResponse({"msg": mensaje, "tipo_res": "error"}, status=500)

def funcion4(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        sl_tipo_responsabilidad = request.POST.get("sl_tipo_responsabilidad")
        descrip_resp = request.POST.get("descrip_resp")
        try:
            cursor = connection.cursor()
            cursor.callproc("RH_AGREGAR_RESPONS", ["erick@sigssmac.com.mx", puesto, sl_tipo_responsabilidad, descrip_resp])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == "RESPONSABILIDAD AGREGADA":
            return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
        else:
            return JsonResponse({"msg": mensaje, "tipo_res": "error"}, status=500)

def funcion5(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        sl_competencia = request.POST.get("sl_competencia")
        sl_dominio = request.POST.get("sl_dominio")
        descrip_comp = request.POST.get("descrip_comp")
        try:
            cursor = connection.cursor()
            cursor.callproc("RH_AGREGAR_COMP_GEN", ["erick@sigssmac.com.mx", puesto, sl_competencia, int(sl_dominio), descrip_comp])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == "COMPETENCIA AGREGADA A PUESTO ACTUAL":
            return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
        else:
            return JsonResponse({"msg": mensaje, "tipo_res": "error"}, status=500)

def funcion6(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        comp_tec = request.POST.get("comp_tec")
        dom_tec = request.POST.get("sl_dominio")
        desc_tec = request.POST.get("desc_tec")
        try:
            cursor = connection.cursor()
            cursor.callproc("RH_AGREGAR_COMP_TEC_HAB_D", ["erick@sigssmac.com.mx", puesto, "Competencia", comp_tec,  desc_tec, int(dom_tec)])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == "COMPETENCIA TECNICA/HABILIDAD AGREGADA CORRECTAMENTE":
            return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
        else:
            return JsonResponse({"msg": mensaje, "tipo_res": "error"}, status=500)

def funcion7(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        habilidad = request.POST.get("habilidad")
        desc_hab = request.POST.get("desc_hab")
        dom_hab = request.POST.get("sl_dominio")
        try:
            cursor = connection.cursor()
            cursor.callproc("RH_AGREGAR_COMP_TEC_HAB_D", ["erick@sigssmac.com.mx", puesto, "Habilidad", habilidad, desc_hab, dom_hab])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == "COMPETENCIA TECNICA/HABILIDAD AGREGADA CORRECTAMENTE":
            return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
        else:
            return JsonResponse({"msg": mensaje, "tipo_res": "error"}, status=500)

def funcion8(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        area_trab = request.POST.get("area_trab")
        peligro = request.POST.get("peligro")
        riesgo = request.POST.get("riesgo")
        nivel = request.POST.get("nivel")
        epp = request.POST.get("epp")
        try:
            cursor = connection.cursor()
            cursor.callproc("RH_AGREGAR_ASP_SSMAC", ["erick@sigssmac.com.mx", puesto, area_trab, peligro, riesgo, nivel, epp])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == "ASPECTO SSMAC AGREGADO":
            return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
        else:
            return JsonResponse({"msg": mensaje, "tipo_res": "error"}, status=500)

def funcion9(request):
    if request.method == 'POST':
        puesto = request.POST.get("puesto")
        sl_tipo_esf = request.POST.get("sl_tipo_esf")
        desc_esf = request.POST.get("desc_esf")
        try:
            cursor = connection.cursor()
            cursor.callproc("RH_AGREGAR_REQ_FISICOS", ["erick@sigssmac.com.mx", puesto, sl_tipo_esf, desc_esf])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
            if mensaje == "REQUERIMIENTO FISICO AGREGADO CORRECTAMENTE":
                return JsonResponse({"msg": mensaje, "tipo_res": "success"}, status=200)
            else:
                return JsonResponse({"msg": "Datos no almacenados", "tipo_res": "error"}, status=500)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()


def crear_directorio(request):
    if request.method == 'POST' and request.is_ajax():
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("AGREGAR_EMPLEADO_V2", [request.session.get("email"), "", request.POST.get("nombre_emp"), request.POST.get("ap_paterno"), request.POST.get("ap_materno"), request.POST.get("sl_puesto"),request.POST.get("fecha_registro"), request.POST.get("edad"), request.POST.get("grado_estudio"), request.POST.get("direccion"), request.POST.get("sl_sexo"), request.POST.get("estado"), request.POST.get("tipo_sangre"), request.POST.get("cont_emergencia"), request.POST.get("emergencia"), request.POST.get("experiencia"), request.POST.get("cap_requerida"), request.POST.get("nss"), request.POST.get("curp"), request.POST.get("rfc"), request.POST.get("correo"), request.POST.get("celular")])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == 'CARACTERISTICAS AGREGADAS A EL EMPLEADO':
            return JsonResponse({"bg_msg": "Datos enviados","msg": mensaje, "state": "success"}, status=200)
        else:
            return JsonResponse({"bg_msg": "Error ocurrido", "msg": mensaje, "state": "error"}, status=200)

def subir_imagen(request):
    if request.method == 'POST':
        mensaje = ""
        try:
            imagen = request.FILES["imagen"]
            cursor = connection.cursor()
            cursor.callproc("GUARDAR_IMAGEN", ["erick@sigssmac.com.mx", imagen.name, imagen, "Empleado", request.POST.get("empleado")])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except (OperationalError, IntegrityError):
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == "IMAGEN AGREGADA":
            return JsonResponse({ "status": "success", "msg": "Exito", "msg_salida": mensaje }, status=200)
        else:
            mensaje = "Imagen no se pudo guardar"
            return JsonResponse({ "status": "error", "msg": "Error", "msg_salida": mensaje }, status=200)
    else:
        mensaje = "La imagen no puede ser leida"
        return JsonResponse({ "status": "error", "msg": "Error", "msg_salida": mensaje }, status=500)

def actualizar_perfil(request):
    if request.method == 'POST':
        mensaje = ""
        print("Estoy en el post")
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", request.POST.get("opcion"), request.POST.get("puesto_sel"), "", "", request.POST.get("formacion"), request.POST.get("escolaridad"), request.POST.get("perfil_p"), request.POST.get("experiencia"), "", ""])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except (OperationalError, IntegrityError):
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == 'PERFIL ACADEMICO / PROFESIONAL ACTUALIZADO':
            return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
        else:
            return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
    else:
        print("No stoy en el post")
        return JsonResponse({"": ""}, status=200)

def actualizar_gen(request):
    if request.method == 'POST':
        print("Estoy en el post")
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", request.POST.get("opcion"), request.POST.get("puesto_sel"), request.POST.get("nombre_puesto"), request.POST.get("objetivo"), "", "", "", "", "", ""])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == 'OBJETIVO ACTUALIZADO':
            return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
        else:
            return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
    else:
        print("No estoy en el post")
        return JsonResponse({"": ""}, status=500)

def eliminar_subordinado(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", request.POST.get("opcion"), request.POST.get("id_p"), "", "", "", "", "", "", request.POST.get("sub"), ""])
            mensaje = cursor.fetchall()[0][0]
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == 'SUPERVISION ELIMINADA':
            return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
        else:
            return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
    else:
        return JsonResponse({"": ""}, status=500)

def eliminar_supervisor(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", request.POST.get("opcion"), request.POST.get("id_p"), "", "", "", "", "", "", request.POST.get("sup"), ""])
            mensaje = cursor.fetchall()[0][0]
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == 'SUBORDINACION ELIMINADA DEL PUESTO':
            return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
        else:
            return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
    else:
        return JsonResponse({"": ""}, status=500)

def eliminar_funcion(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", request.POST.get("opcion"), request.POST.get("id_p"), "", "", "", "", "", "", "", request.POST.get("funcion")])
            mensaje = cursor.fetchall()[0][0]
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == 'FUNCION ELIMINADA DEL PUESTO':
            return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
        else:
            return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
    else:
        return JsonResponse({"": ""}, status=500)

def eliminar_res_ad(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", "ELIMINAR RESP ADQ", request.POST.get("id_p"), "", "", "", "", "", "", "", request.POST.get("res_ad")])
            mensaje = cursor.fetchall()[0][0]
            if mensaje == 'OBJETIVO ACTUALIZADO':
                return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
            else:
                return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
    else:
        return JsonResponse({"": ""}, status=500)

def eliminar_com_gen(request):
    if request.method == 'POST':
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", "ELIMINAR COMP GEN", request.POST.get("id_p"), "", "", "", "", "", "", "", request.POST.get("comp_g")])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
            if mensaje == 'COMPETENCIA GENERICA ELIMINADA DEL PUESTO':
                return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
            else:
                return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=200)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
    else:
        return JsonResponse({"": ""}, status=500)

def eliminar_com_tec(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", "ELIMINAR COMP TEC", request.POST.get("id_p"), "", "", "", "", "", "", "", request.POST.get("comp_t")])
            mensaje = cursor.fetchall()[0][0]
            print(mensaje)
            if mensaje == 'COMPETENCIA/HABILIDAD ELIMINADA DEL PUESTO':
                return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
            else:
                return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
    else:
        return JsonResponse({"": ""}, status=500)

def eliminar_asp_ssmac(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", "ELIMINAR ASP SSMAC", request.POST.get("id_p"), "", "", "", "", "", "", "", request.POST.get("aspecto")])
            mensaje = cursor.fetchall()[0][0]
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == 'ASPECTOS ELIMINADOS DEL PUESTO':
            return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
        else:
            return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
    else:
        return JsonResponse({"": ""}, status=500)

def eliminar_requer_fis(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICAR_ELIMINAR_PP", ["erick@sigssmac.com.mx", "ELIMINAR REQ FIS", request.POST.get("id_p"), "", "", "", "", "", "", "", request.POST.get("req")])
            mensaje = cursor.fetchall()[0][0]
        except OperationalError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        except IntegrityError:
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje == 'REQUERIMIENTOS FISICOS ELIMINADOS DEL PUESTO':
            return JsonResponse({"msg": "Éxito", "msg_salida": mensaje, "status": "success"}, status=200)
        else:
            return JsonResponse({"msg": "Error", "msg_salida": "El perfil no pudo ser actualizado", "status": "error"}, status=500)
    else:
        return JsonResponse({"": ""}, status=500)
    