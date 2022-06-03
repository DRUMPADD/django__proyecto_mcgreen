from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db import IntegrityError, OperationalError, InternalError, connection

def directorio_perfil(request):
    if request.session.get("email"):
        puestos = ""
        departamentos = ""
        empleados = ""
        try:
            cursor = connection.cursor()
            puestos = cursor.execute("SELECT * from app_puestos")
            puestos = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * from app_departamento")
            departamentos = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * from app_empleados where id_empleado != 'ERICK' and id_empleado != 'RDHI-1234' and id_empleado != 'SIGSSMAC-JEFE'")
            empleados = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        context = {
            'privilegio': request.session.get("privilegio"),
            'puestos': puestos,
            'departamentos': departamentos,
            'departamento': request.session.get("departamento"),
            'empleados': empleados,
            "email": request.session.get("email"),
        }
        return render(request, 'RRHH/directorio_perfil.html', context)
    else:
        return redirect("/cerrar_sesion")

def mostrar_perfil_url(request, nombre_perfil=""):
    if request.session.get("email"):
        if nombre_perfil != "":
            try:
                sup = connection.cursor()
                sup.callproc("MOSTRAR_PUESTOS_V2_SUPERVISAR", [nombre_perfil])
                supervisar = sup.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                sup.close()
            
            try:
                supviso = connection.cursor()
                supviso.callproc("MOSTRAR_PUESTOS_V2_TSUPERVISAN", [nombre_perfil])
                superviso = supviso.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                supviso.close()
            
            try:
                pe = connection.cursor()
                pe.callproc("MOSTRAR_PUESTOS_V2", [nombre_perfil])
                mas_info = pe.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                pe.close()
            try:
                pe1 = connection.cursor()
                pe1.callproc("MOSTRAR_PUESTOS_V2_P1", [nombre_perfil])
                mas_info1 = pe1.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                pe1.close()
            try:
                pe2 = connection.cursor()
                pe2.callproc("MOSTRAR_PUESTOS_V2_P2", [nombre_perfil])
                mas_info2 = pe2.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                pe2.close()
            try:
                pe3 = connection.cursor()
                pe3.callproc("MOSTRAR_PUESTOS_V2_P3", [nombre_perfil])
                mas_info3 = pe3.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                pe3.close()
            try:
                pe4 = connection.cursor()
                pe4.callproc("MOSTRAR_PUESTOS_V2_P4", [nombre_perfil])
                mas_info4 = pe4.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                pe4.close()
            try:
                pe5 = connection.cursor()
                pe5.callproc("MOSTRAR_PUESTOS_V2_P5", [nombre_perfil])
                mas_info5 = pe5.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                pe5.close()
            try:
                pe6 = connection.cursor()
                pe6.callproc("MOSTRAR_PUESTOS_V2_P6", [nombre_perfil])
                mas_info6 = pe6.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                pe6.close()
            try:
                pe7 = connection.cursor()
                pe7.callproc("MOSTRAR_PUESTOS_V2_P7", [nombre_perfil])
                mas_info7 = pe7.fetchall()
            except (OperationalError, IntegrityError, InternalError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
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
                "privilegio": request.session.get("privilegio"),
            }
            return render(request, 'RRHH/ver_perfil.html', context)
        else:
            return redirect("perfil_y_directorio")
    else:
        return redirect("/cerrar_sesion")

def vista_directorio(request, id_empleado):
    if request.session.get("email"):
        mensaje = ""
        datos = []
        context = {
            "id_emp": id_empleado,
            "mensaje": "",
        }
        try:
            imagen = connection.cursor()
            imagen.callproc("MOSTRAR_IMAGEN",[id_empleado])
            info_img = imagen.fetchall()[0][0]
            print(info_img)
            context["imagen_emp"] = info_img
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            imagen.close()
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_EMPLEADOS_V2", [id_empleado])
            personal_d = cursor.fetchall()
            if not personal_d:
                mensaje = "No existen datos del empleado"
                context["mensaje"] = mensaje
            else:
                datos.append({
                    "nombre": personal_d[0][1],
                    "ap_p": personal_d[0][2],
                    "ap_m": personal_d[0][3],
                    "fecha_nac": personal_d[0][21],
                    "edad": personal_d[0][6],
                    "genero": personal_d[0][9],
                    "grado_estudio": personal_d[0][7],
                    "direccion": personal_d[0][8],
                    "edo_civil": personal_d[0][10],
                    "tipo_sangre": personal_d[0][11],
                    "contacto": personal_d[0][12],
                    "numero": personal_d[0][13],
                    "fec_registro": personal_d[0][4],
                    "experiencia": personal_d[0][14],
                    "capacitacion": personal_d[0][15],
                    "nss": personal_d[0][16],
                    "curp": personal_d[0][17],
                    "rfc": personal_d[0][18],
                    "correo": personal_d[0][19],
                    "tel_celular": personal_d[0][20],
                })
                context["emp_datos"] = datos
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        return render(request, "RRHH/ver_personal.html", context)
    else:
        return redirect("/cerrar_sesion")

def vista_eventos(request):
    if request.session.get("email") and request.session.get("privilegio") != 'EMPLEADO':
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_TODOS_LOS_EVENTOS")
            eventos = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
        finally:
            cursor.close()
        
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_TODAS_LAS_ACTIVIDADES")
            actividades = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        context = {
            'eventos': eventos,
            'actividades': actividades,
            'email': request.session.get("email"),
            'privilegio': request.session.get("privilegio"),
        }
        return render(request, "RRHH/eventos.html", context)
    else:
        return redirect("/cerrar_sesion")

def rrhh_detalles(request):
    mensaje = ""
    puestos = ""
    empleados = ""
    total_puestos = 0
    total_empleados = 0
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * from app_puestos")
        puestos = cursor.fetchall()
        for puesto in range(0, len(puestos)):
            total_puestos = total_puestos + 1
    except (OperationalError, IntegrityError, InternalError) as e:
        print(e)
        return render(request, "errors/error500.html", {
            "mensaje": "Contacte con el servicio de sistemas"
        })
    finally:
        cursor.close()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * from app_empleados where id_empleado != 'ERICK' and id_empleado != 'RDHI-1234' and id_empleado != 'SIGSSMAC-JEFE'")
        empleados = cursor.fetchall()
        for emp in range(0, len(empleados)):
            total_empleados = total_empleados + 1
    except (OperationalError, IntegrityError, InternalError) as e:
        print(e)
        return render(request, "errors/error500.html", {
            "mensaje": "Contacte con el servicio de sistemas"
        })
    finally:
        cursor.close()
    try:
        cursor = connection.cursor()
        cursor.callproc("RRHH_DETALLES")
        mensaje = cursor.fetchall()
    except (OperationalError, IntegrityError, InternalError) as e:
        print(e)
        return JsonResponse({"status": "error", "msg": "No se pueden mostrar los datos"}, status=200)
    return JsonResponse({"status": "success", "msg": mensaje, "total_puestos": total_puestos, "total_empleados": total_empleados}, status=200)