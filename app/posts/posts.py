import io, datetime
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError, InternalError, OperationalError, connection
from ..forms import formulario_cliente, formulario_proveedor, Formulario_registro
# from openpyxl import Workbook
# from openpyxl.styles import Font
# from openpyxl.styles.alignment import Alignment
# from openpyxl.styles.borders import BORDER_THIN, Border, Side
import xlwt
import xlsxwriter

def registra_usuario(request):
    if request.session.get('email'):
        if request.method == 'POST':
            formulario = Formulario_registro(request.POST)
            if formulario.is_valid():
                try:
                    cursor = connection.cursor()
                    ext_email = formulario["slemail"].value()
                    cursor.callproc("AGREGAR_USUARIO",[request.session.get("email"), formulario["matricula"].value(),formulario["nombre_usuario"].value(),formulario["ap_p"].value(),formulario["ap_m"].value(),formulario["sl_puestos"].value(),formulario["email"].value()+ext_email,formulario["contra"].value(),formulario["rol"].value()])
                    mensaje = cursor.fetchall()[0][0]
                    print(mensaje)
                except (OperationalError, IntegrityError) as e:
                    print(e)
                    return render(request, "errors/error500.html", {
                        "mensaje": "Contacte con el servicio de sistemas"
                    })
                finally:
                    cursor.close()
                if mensaje != 'USUARIO CREADO':
                    messages.error(request, mensaje)
                else:
                    messages.success(request, "El usuario ha sido creado éxitosamente")
                return redirect("/Registro")
            else:
                print(formulario.errors)
                return redirect("/Registro")
    else:
        return redirect("/Registro")

def crear_evento(request):
    if request.method == 'POST' and request.is_ajax():
        fecha = request.POST.get("fecha_evento")
        opcion = request.POST.get("opciones")
        usuarios = request.POST.getlist("sl_usuarios")
        nombre_evento = request.POST.get("evento_nombre")
        descripcion = request.POST.get("descripcion_evento")
        prioridad = request.POST.get("sl_prioridades")

        print(opcion)
        print(fecha)
        print(nombre_evento)
        print(descripcion)
        print(prioridad)

        if opcion == 'TODO EL PERSONAL':
            mensaje = ""
            try:
                cursor = connection.cursor()
                cursor.callproc("CREAR_EVENTO", [request.session.get("email"), opcion, nombre_evento, descripcion, fecha, prioridad])
                mensaje = cursor.fetchall()[0][0]
            except (InternalError, OperationalError) as e:
                print(e)
                return JsonResponse({"status": "error", "mensaje": "Error al realizar el procedimiento"}, status=200)
            finally:
                cursor.close()
            return JsonResponse({"status": "success", "mensaje": mensaje}, status=200)
        elif opcion == 'EVENTO' or opcion == 'ACTIVIDAD':
            ids_creados = []
            print(usuarios)
            for i in range(0, len(usuarios)):
                try:
                    cursor = connection.cursor()
                    cursor.callproc("CREAR_EVENTO", [request.session.get("email"), opcion, nombre_evento, descripcion, fecha, prioridad])
                    id_creado = cursor.fetchall()[0][0]
                    print(id_creado)
                    ids_creados.append(id_creado)
                except (InternalError, OperationalError) as e:
                    print(e)
                    return JsonResponse({"status": "error", "mensaje": "Error al realizar el procedimiento de crear evento"}, status=200)
                finally:
                    cursor.close()
            mensaje = ""
            for i in range(0, len(ids_creados)):
                try:
                    asignar_evento = connection.cursor()
                    asignar_evento.callproc("ASIGNAR_EVENTO", [request.session.get("email"), ids_creados[i], usuarios[i]])
                    mensaje = asignar_evento.fetchall()[0][0]
                    print(mensaje)
                except (InternalError, OperationalError) as e:
                    print(e)
                    return JsonResponse({"status": "error", "mensaje": "Error al realizar el procedimiento de asignar evento"}, status=200)
                finally:
                    asignar_evento.close()
            return JsonResponse({"status": "success", "mensaje": mensaje}, status=200)
        else:
            return JsonResponse({"status": "error", "mensaje": "Debe elegir alguna de las 3 opciones"}, status=200)
    else:
        return JsonResponse({"status": "error", "mensaje": "La petición falló"}, status=200)

def agregar_producto(request):
    if request.session.get('email'):
        if request.method == 'POST':
            mensaje = ""
            if request.POST.get("producto") is not None and request.POST.get("descripcion") is not None and request.POST.get("cantidad") is not None and request.POST.get("ddw_medidas") is not None and request.POST.get("ddw_departamentos") is not None and request.POST.get("precio") is not None and request.POST.get("sl_tipo_cambio") is not None and request.POST.get("sucursal") is not None and request.session.get("email") is not None:
                try:
                    cursor = connection.cursor()
                    cursor.callproc("Agrega_INV", [request.POST["producto"], request.POST["descripcion"], request.POST["cantidad"], request.POST["ddw_medidas"], request.POST["ddw_departamentos"], request.POST["precio"], request.POST["sl_tipo_cambio"], request.POST["sucursal"], request.session.get("email")])
                    mensaje = cursor.fetchall()[0][0]
                    print(mensaje)
                    if mensaje != 'EXISTENCIAS AGREGADAS CORRECTAMENTE' and mensaje != 'FACTURA DISPONIBLE':
                        messages.error(request, "Ocurrió un error al hacer la modificación")
                    else:
                        messages.success(request, "Producto registrado con éxito")
                except (OperationalError, IntegrityError):
                    return render(request, "errors/error500.html", {
                        "mensaje": "Contacte con el servicio de sistemas"
                    })
                finally:
                    cursor.close()
            else:
                messages.error(request, "Debe llenar todos los campos")
            return redirect("/Inventario_general")
    else:
        return redirect("/cerrar_sesion")

def modificar_producto(request):
    if request.method == 'POST':
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICA_INV", [request.session.get('email'), request.POST["id_producto"], request.POST["producto"], request.POST["descripcion"], request.POST["precio"]])
            mensaje = cursor.fetchall()[0][0]
        except (OperationalError, IntegrityError):
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje != 'EL PRECIO FUE MODIFICADO CORRECTAMENTE':
            messages.error(request, "Ocurrió un error al hacer la modificación")
        else:
            messages.success(request, "Elementos actualizados con éxito")
        return redirect("/Inventario_general")

def modificar_producto_cantidad(request):
    if request.method == 'POST':
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("MODIFICA_INV_ADMIN", [request.session.get('email'), request.POST["id_producto"], request.POST["producto"], request.POST["descripcion"], request.POST["precio"], request.POST["cantidad"]])
            mensaje = cursor.fetchall()[0][0]
        except (OperationalError, IntegrityError):
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje != 'EL PRECIO FUE MODIFICADO CORRECTAMENTE':
            messages.error(request, "Ocurrió un error al hacer la modificación")
        else:
            messages.success(request, "Elementos actualizados con éxito")
        return redirect("/Inventario_general")

def descontinuar_producto(request,id_prod):
    if request.session.get("email"):
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("DESCONTINUAR_PRODUCTO", [id_prod, request.session.get("email")])
            mensaje = cursor.fetchall()[0][0]
        except (OperationalError, IntegrityError):
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje != 'EL PRODUCTO: ' + id_prod + ' FUE DESCONTINUADO':
            messages.error(request, "Ocurrió un error al eliminar el producto")
        else:
            messages.error(request, "Producto eliminado")
        return redirect("/Inventario_general")
    else:
        return redirect("/cerrar_sesion")

def activar_producto(request,id_prod):
    if request.session.get("email"):
        mensaje = ""
        try:
            cursor = connection.cursor()
            cursor.callproc("ACTIVAR_PRODUCTO", [request.session.get('email'), id_prod])
            mensaje = cursor.fetchall()[0][0]
        except (OperationalError, IntegrityError):
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        if mensaje != 'EL PRODUCTO: ' + id_prod + ' FUE ACTIVADO':
            messages.error(request, "Ocurrió un error al activar el producto")
        else:
            messages.success(request, "Producto activado")
        return redirect("/Inventario_general")
    else:
        return redirect("/cerrar_sesion")

# def generar_compra(request):
#     if request.session.get('email'):
#         if request.method == 'POST':
#             cursor = connection.cursor()
#             cursor.callproc("COMPRA",[request.POST["sl_productos"], request.POST["comprador"], request.POST["cantidad"], request.POST["p_u"], request.POST["fecha_compra"], request.POST["sl_proveedores"], request.POST["motivo"]])
#             mensaje = cursor.fetchall()
#             print(mensaje)
#             # if mensaje != 'FACTURA DISPONIBLE':
#             #     messages.error(request, "Ocurrió un error al realizar la compra")
#             # else:
#             #     messages.success(request, "Compra registrada")
#             cursor.close()
#             return redirect("/Compras")
#     else:
#         return redirect("/cerrar_sesion")
def generar_compra(request):
    if request.method == 'POST' and request.is_ajax():
        datos = []
        comprador = request.POST.get("comprador")
        fecha_compra = request.POST.get("fecha_compra")
        motivo = request.POST.get("motivo")
        articulo = request.POST.get("articulo")
        sl_proveedores = request.POST.getlist("sl_proveedores")
        sl_productos = request.POST.getlist("sl_productos")
        cantidades = request.POST.getlist("cantidad")
        densidades = request.POST.getlist("densidad")
        p_u = request.POST.getlist("p_u")
        mensaje_c1 = ""
        mensaje_c2 = ""
        mensaje_c3 = ""
        try:
            compra_1 = connection.cursor()
            compra_1.callproc("COMPRA_p1", [comprador, fecha_compra, motivo])
            mensaje_c1 = str(compra_1.fetchall()[0][0]).split(": ")[1]
            print("Mensaje compra 1:",mensaje_c1)
        except (IntegrityError, OperationalError):
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            compra_1.close()
        
        print(fecha_compra != None)
        print(sl_proveedores != None)
        print(sl_productos != None)
        print(cantidades != None)
        print(p_u != None)

        if comprador != None and fecha_compra != None and motivo != None and articulo != None and sl_proveedores != None and sl_productos != None and cantidades != None and p_u != None:
            print("Entro al if")
            try:
                if mensaje_c1 != None:
                    for i in range(0,int(articulo)):
                        datos.append({
                            "comprador": comprador,
                            "fecha_compra": fecha_compra,
                            "motivo": motivo,
                            "articulo": i + 1,
                            "sl_proveedores": sl_proveedores[i],
                            "sl_productos": sl_productos[i],
                            "cantidades": float(cantidades[i]),
                            "densidades": float(densidades[i]),
                            "p_u": p_u[i],
                        })
                    for i in range(len(datos)):
                        try:
                            compra_2 = connection.cursor()
                            print("Posición", i)
                            print(datos[i]["comprador"])
                            print(datos[i]["fecha_compra"])
                            print(datos[i]["motivo"])
                            print(datos[i]["articulo"])
                            print(datos[i]["sl_proveedores"])
                            print(datos[i]["sl_productos"])
                            print(datos[i]["cantidades"])
                            print(datos[i]["p_u"])
                            compra_2.callproc("COMPRA_p2", [datos[i]["sl_productos"], mensaje_c1, i + 1, datos[i]["cantidades"] * datos[i]["densidades"], datos[i]["p_u"], datos[i]["sl_proveedores"]])
                            mensaje_c2 = compra_2.fetchall()[0][0]
                            compra_2.close()
                        except (OperationalError, IntegrityError):
                            return render(request, "errors/error500.html", {
                                "mensaje": "Contacte con el servicio de sistemas"
                            })
                    print("Mensaje compra_c2:", mensaje_c2)
                    if mensaje_c2 != "":
                        try:
                            compra_3 = connection.cursor()
                            compra_3.callproc("COMPRA_p3", [comprador, mensaje_c1])
                            mensaje_c3 = compra_3.fetchall()[0][0]
                            print("Mensaje compra 3:",mensaje_c3)
                        except (OperationalError, IntegrityError):
                            return render(request, "errors/error500.html", {
                                "mensaje": "Contacte con el servicio de sistemas"
                            })
                        finally:
                            compra_3.close()
                    else:
                        print("No se realizó la compra 2")
                else:
                    print("No se realizó la compra 1")
            except (OperationalError, IntegrityError):
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
        else:
            print("Están vacíos")
        if mensaje_c3 == 'FACTURA DISPONIBLE':
            return JsonResponse({"status": "success","msg": "Compra realizada", "msg_compra": mensaje_c3}, status=200)
        else:
            return JsonResponse({"status": "error", "msg": "Problema ocurrido", "msg_compra": "No se pudo realizar la compra"}, status=200)

def generar_venta(request):
    if request.session.get('email'):
        if request.method == 'POST':
            try:
                cursor = connection.cursor()
                cursor.callproc("VENTA_MOD",[request.POST["sl_sistemas"].split(' ')[0],request.POST["vendedor"],request.POST["cantidad"],request.POST["p_u"],request.POST["fecha"],request.POST["motivo"],request.POST["sl_clientes"],request.POST["articulo"]])
                print(cursor.fetchall())
            except (OperationalError, IntegrityError):
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
            return redirect("/Ventas")
        else:
            return redirect("/Ventas")
    else:
        return redirect("/cerrar_sesion")


# ?? Sistemas.split
def generar_cuenta_por_cobrar(request):
    if request.session.get('email'):
        if request.method == 'POST':
            sistema = str(request.POST['sl_sistemas']).split(' ')[0]
            cliente = str(request.POST['sl_clientes'])
            mensaje = ""
            if request.POST.get("fecha") != "" and sistema != "" and request.POST.get("pozo") != "" and request.POST.get("total_servicios") != "" and cliente != "":
                try:
                    cursor = connection.cursor()
                    cursor.callproc("VENTA_MOD",[request.POST['email'],request.POST['fecha'],sistema,request.POST['pozo'], request.POST['total_servicios'], request.POST['sl_clientes'], request.POST.get("comentario")])
                    mensaje = cursor.fetchall()[0][0]
                    print(mensaje)

                    return JsonResponse({"status": "success", "msg": mensaje}, status=200)
                except (OperationalError, IntegrityError) as e:
                    print(e)
                    return JsonResponse({"status": "error", "msg": "Error ocurrido en el registro de la venta"}, status=200)
                finally:
                    cursor.close()
            else:
                return JsonResponse({"status": "warning", "msg": "Debe llenar todos los campos"}, status=200)
        else:
            return redirect("/Ventas")
    else:
        return redirect("/cerrar_sesion")

def modificar_cuenta_por_cobrar(request):
    if request.session.get('email'):
        if request.method == 'POST':
            mensaje = ""
            try:
                cursor = connection.cursor()
                cursor.callproc("MODIFICA_VENTA_MOD",[request.POST["id_"], request.POST.get("email"), request.POST.get("fecha_registro"), request.POST.get("pozo"), float(request.POST.get("cantidad_antes")), float(request.POST.get("cantidad_nueva")), request.POST.get("id_producto"), request.POST.get("comentario")])
                mensaje = cursor.fetchall()[0][0]
                print(mensaje)
            except (OperationalError, IntegrityError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
            if mensaje != "CUENTA POR COBRAR MODIFICADA CORRECTAMENTE":
                messages.error(request, "No se pudo realizar la modificación")
            else:
                messages.success(request, "Cuenta por cobrar modificada correctamente")
            cursor.close()
            return redirect("/Ver_cuentas_por_cobrar")
        return redirect("/Ver_cuentas_por_cobrar")
    return redirect("/cerrar_sesion")
    

def agregar_otros(request):
    if request.method == 'POST':
        mensaje = ""
        producto = str(request.POST.get("sl_productos")).split(' ')[0]
        try:
            cursor = connection.cursor()
            cursor.callproc("MOV_INV", [producto, request.POST.get("email"), request.POST.get("cantidad"), request.POST["fecha_otro"], request.POST["motivo"], request.POST["sl_tipo_mov"], request.POST["org_des"]])
            mensaje = cursor.fetchall()[0][0]
        except (OperationalError, IntegrityError) as e:
            print(e)
            return JsonResponse({"status": "error","mensaje": "Error ocurrido, contacte con el servicio de sistemas"}, status=200)
        finally:
            cursor.close()
        if mensaje != 'FACTURA DISPONIBLE':
            return JsonResponse({"status": "error", "mensaje": mensaje}, status=200)
        else:
            return JsonResponse({"status": "success", "mensaje": mensaje}, status=200)

# Proveedores
# def agregar_proveedores(request):
#     if request.session.get('email'):
#         if request.method == 'POST':
#             form = formulario_proveedor(request.POST)
#             if form.is_valid():
#                 cursor = connection.cursor()
#                 cursor.callproc("Agrega_Proveedor",[request.session.get('email'), form["RFC"].value(),form["proveedor"].value(),form["telefono"].value(),form["email"].value()])
#                 cursor.close()
#                 return redirect("/Compras")    
#         return redirect("/Compras")
#     else:
#         return redirect("/cerrar_sesion")

def agregar_proveedores(request):
    if request.session.get('email'):
        if request.method == 'POST':
            mensaje = ""
            try:
                cursor = connection.cursor()
                cursor.callproc("Agrega_Proveedor",[request.session.get('email'), request.POST.get("RFC"),request.POST.get("proveedor"),request.POST.get("telefono"),request.POST.get("email"), request.POST.get("sector")])
                mensaje = cursor.fetchall()[0][0]
                print(mensaje)
            except (OperationalError, IntegrityError):
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
            if mensaje == 'PROVEEDOR Insertado Correctamente':
                return JsonResponse({"status": "success", "msg": "Operación exitosa", "msg_salida": mensaje}, status=200)
            else:
                return JsonResponse({"status": "warning", "msg": "Error", "msg_salida": mensaje}, status=200)
    else:
        return redirect("/cerrar_sesion")

def agregar_clientes(request):
    if request.session.get('email'):
        if request.method == 'POST':
            mensaje = ""
            form = formulario_cliente(request.POST)
            if request.POST.get("Identificador") is not None and request.POST.get("cliente") is not None and request.POST.get("direccion") is not None and request.POST.get("telefono") is not None and request.POST.get("email") is not None:
                if form.is_valid():
                    try:
                        cursor = connection.cursor()
                        cursor.callproc("Agrega_CLIENTE",[form["Identificador"].value(), form["cliente"].value(), form["direccion"].value(), form["telefono"].value(), form["email"].value()])
                        mensaje = cursor.fetchall()[0][0]
                        print(mensaje)
                    except (OperationalError, IntegrityError):
                        return render(request, "errors/error500.html", {
                            "mensaje": "Contacte con el servicio de sistemas"
                        })
                    finally:
                        cursor.close()
                    if mensaje == 'Cliente insertado correctamente':
                        messages.success(request, "Nuevo cliente agregado")
                    else:
                        messages.error(request, "No se pudo agregar el cliente")
                else:
                    messages.error(request, "Debe llenar los campos con la información que se le pide")
            else:
                messages.error(request, "Debe llenar todos los campos")
                return redirect("/Ventas")    
        return redirect("/Ventas")
    else:
        return redirect("/cerrar_sesion")



# ?? Registrar sistema
def registrar_sistema(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        motivo = request.POST.get("motivo")
        descripcion = request.POST.get("descripcion")
        departamento = request.POST.get("sl_departamentos")
        tipo_cambio = request.POST.get("tipo_cambio")
        sucursal = request.POST.get("sucursal")
        precio = request.POST.get("precio")
        fecha = request.POST.get("fecha")
        productos = request.POST.getlist("sl_producto")
        cantidades = request.POST.getlist("cantidad")

        ar_productos = []
        ar_nom_productos = []
        ar_cantidades = []

        for i in range(0, len(productos)):
            p_ = str(productos[i]).split(' ')
            ar_nom_productos.append(p_[0])
            ar_productos.append(' '.join(p_[2:]))
            ar_cantidades.append(float(p_[1]))
        
        msg_cantidad_pasada = ""

        for i in range(0, len(ar_productos)):
            if float(cantidades[i]) > ar_cantidades[i]:
                msg_cantidad_pasada = "El producto {0} tiene una cantidad menor a la que se necesita\nCantidad actual: {1}".format(ar_productos[i], ar_cantidades[i])
                print(msg_cantidad_pasada)
                break
        comprobar_producto_activo = ""
        if msg_cantidad_pasada == '':
            for i in range(0, len(ar_nom_productos)):
                try:
                    transformacion1 = connection.cursor()
                    transformacion1.callproc("TRANSFORMACION_P1", [email, ar_nom_productos[i], cantidades[i], motivo, fecha])
                    comprobar_producto_activo = transformacion1.fetchall()[0][0]
                    print(comprobar_producto_activo)
                except (OperationalError, IntegrityError):
                    return render(request, "errors/error500.html", {
                        "mensaje": "Contacte con el servicio de sistemas"
                    })
                finally:
                    transformacion1.close()
                if comprobar_producto_activo == "EL PRODUCTO: "+ ar_nom_productos[0] +" A ESTA DESACTIVADO, NO ES POSIBLE REALIZAR SALIDAS DE DICHO PRODUCTO, ACTIVELO O REALIZE UN INGRESO":
                    break
            sistema = request.POST.get("nombre_sistema")
            sistema_n = request.POST.get("nuevo_nombre_sistema")
            c_sistema = request.POST.get("cantidad_sistema")
            mensaje = ""

            if comprobar_producto_activo != "":
                if sistema != '' or sistema_n != '':
                    if sistema_n != '':
                        try:
                            transformacion2 = connection.cursor()
                            transformacion2.callproc("TRANSFORMACION_P2", [email, sistema_n, descripcion, departamento, precio, tipo_cambio, sucursal, "", c_sistema, "", ""])
                            mensaje = transformacion2.fetchall()[0][0]
                            print(mensaje)
                        except (OperationalError, IntegrityError):
                            return render(request, "errors/error500.html", {
                                "mensaje": "Contacte con el servicio de sistemas"
                            })
                        finally:
                            transformacion2.close()
                    else:
                        try:
                            transformacion2 = connection.cursor()
                            transformacion2.callproc("TRANSFORMACION_P2", [email, "", "", "", "", "", "", sistema, c_sistema, motivo, fecha])
                            mensaje = transformacion2.fetchall()[0][0]
                            print(mensaje)
                        except (OperationalError, IntegrityError):
                            return render(request, "errors/error500.html", {
                                "mensaje": "Contacte con el servicio de sistemas"
                            })
                        finally:
                            transformacion2.close()
                    if mensaje == 'SISTEMA CREADO CORRECTAMENTE' or mensaje == 'FACTURA DISPONIBLE' or mensaje == 'EXISTENCIAS AGREGADAS CORRECTAMENTE':
                        return JsonResponse({"status": "success", "msg_salida": "Sistema creado con éxito"}, status=200)
                    else:
                        return JsonResponse({"status": "error", "msg_salida": "El sistema no pudo ser creado\n Intente de nuevo"}, status=200)
                else:
                    return JsonResponse({"status": "warning", "msg_salida": "<p>Debe dar un nombre al sistema o elegir uno</p>"}, status=200)
            else:
                return JsonResponse({"status": "warning", "msg_salida": comprobar_producto_activo}, status=200)
        else:
            return JsonResponse({"status": "warning", "msg_salida": msg_cantidad_pasada}, status=200)
    else:
        return JsonResponse({"status": "error", "msg_salida": "No se pudo realizar dicha acción"}, status=200)



def exportar_inventario_xls(request):
    fecha_hoy = datetime.datetime.now()
    hoy = str(fecha_hoy.month) + "-" + str(fecha_hoy.day) + "-" + str(fecha_hoy.year)
    cursor = connection.cursor()
    cursor.callproc("MOSTRAR_PRODUCTOS_ACTIVOS")
    resultado = cursor.fetchall()
    workbook = xlwt.Workbook()
    hoja_1 = workbook.add_sheet('Inventario', cell_overwrite_ok=True)
    font_encabezado = xlwt.Font()
    font_cuerpo = xlwt.Font()
    
    font_encabezado.name = 'Arial'
    font_encabezado.bold = True
    font_encabezado.height = 10 * 10
    font_cuerpo.name = 'Arial'
    font_encabezado.height = 15 * 15

    estilo_encabezado = xlwt.XFStyle()
    estilo_cuerpo = xlwt.XFStyle()
    estilo_encabezado.font = font_encabezado
    estilo_cuerpo.font = font_cuerpo
    bordes = xlwt.Borders()
    bordes.left = 1
    bordes.right = 1
    bordes.top = 1
    bordes.bottom = 1
    estilo_encabezado.borders = bordes
    estilo_cuerpo.borders = bordes

    # comienzo Estilos celdas de encabezado
    imagen = xlwt.Borders()
    imagen.left = 1
    imagen.right = 1
    imagen.top = 1
    imagen.bottom = 1
    titulo = xlwt.Font()
    titulo_xfs = xlwt.XFStyle()
    titulo_alineado = xlwt.Alignment()
    titulo_alineado.horz = xlwt.Alignment.HORZ_CENTER
    titulo_alineado.vert = xlwt.Alignment.VERT_CENTER
    titulo.name = 'Arial'
    titulo.bold = True
    titulo.height = 18 * 18
    titulo.colour_index = xlwt.Style.colour_map["green"]
    titulo_xfs.font = titulo
    titulo_xfs.borders = bordes
    titulo_xfs.alignment = titulo_alineado
    pagina = xlwt.Font()
    pagina_xfs = xlwt.XFStyle()
    pagina.name = 'Arial'
    pagina.bold = True
    pagina.height = 15 * 15
    pagina_xfs.colour_index = xlwt.Style.colour_map["black"]
    pagina_xfs.font = pagina
    pagina_xfs.borders = bordes
    pagina_xfs.alignment = titulo_alineado
    estilo_encabezado.alignment = titulo_alineado

    border_celdas_vacias = xlwt.Borders()
    border_celdas_vacias_xfs = xlwt.XFStyle()
    border_celdas_vacias.left = 1
    border_celdas_vacias.right = 1
    border_celdas_vacias.top = 1
    border_celdas_vacias.bottom = 1
    border_celdas_vacias_xfs.borders = border_celdas_vacias
    border_celdas_vacias_pagina = xlwt.Borders()
    border_celdas_vacias_pagina_xfs = xlwt.XFStyle()
    border_celdas_vacias_pagina.left = 1
    border_celdas_vacias_pagina.right = 1
    border_celdas_vacias_pagina.top = 1
    border_celdas_vacias_pagina.bottom = 1
    border_celdas_vacias_pagina_xfs.borders = border_celdas_vacias
    border_celdas_vacias_pagina_xfs.alignment = titulo_alineado

    hoja_1.write_merge(0, 3, 0, 1, "", titulo_xfs)
    hoja_1.write_merge(0, 1, 2, 8, "Fluidos McGreen de México S.A de C.V", titulo_xfs)
    hoja_1.write_merge(2, 3, 2, 8, "Inventario general", titulo_xfs)
    hoja_1.write(0, 9, "Código:", estilo_encabezado)
    hoja_1.write(1, 9, "Revisión:", estilo_encabezado)
    hoja_1.write_merge(2, 3, 9, 9, "Fecha de revisión:", pagina_xfs)
    hoja_1.write(0, 10, "MG-FO-ADM-005", border_celdas_vacias_xfs)
    hoja_1.write(1, 10, "00", border_celdas_vacias_xfs)
    hoja_1.write_merge(2, 3, 10, 10, "01-02-2022", border_celdas_vacias_pagina_xfs)
    # fin
    
    # campos del encabezado de la tabla
    hoja_1.write(4, 0, "Identificador", estilo_cuerpo)
    hoja_1.write(4, 1, "Nombre", estilo_cuerpo)
    hoja_1.write(4, 2, "Descripción", estilo_cuerpo)
    hoja_1.write(4, 3, "Cantidad", estilo_cuerpo)
    hoja_1.write(4, 4, "Medida", estilo_cuerpo)
    hoja_1.write(4, 5, "Departamento", estilo_cuerpo)
    hoja_1.write(4, 6, "Precio unitario", estilo_cuerpo)
    hoja_1.write(4, 7, "Subtotal", estilo_cuerpo)
    hoja_1.write(4, 8, "Precio total", estilo_cuerpo)
    hoja_1.write(4, 9, "Tipo de cambio", estilo_cuerpo)
    hoja_1.write(4, 10, "Sucursal", estilo_cuerpo)
    # fin
    
    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 11):
            hoja_1.write(fila, col, u'%s' % resultado[row - 1][col], estilo_cuerpo)
        fila = 1 + fila
    nombre_archivo ="Inventario.xls"
    response = HttpResponse(content_type="application/Excel") 
    contenido = "attachment; filename={0}".format(nombre_archivo)
    response["Content-Disposition"] = contenido
    response["ContentType"] = "application/vnd.ms-excel"
    workbook.save(response)
    cursor.close()
    return response

def exportar_inventario_xlsx(request):
    fecha_hoy = datetime.datetime.now()
    hoy = str(fecha_hoy.month) + "-" + str(fecha_hoy.day) + "-" + str(fecha_hoy.year)
    output = io.BytesIO()
    cursor = connection.cursor()
    cursor.callproc("MOSTRAR_PRODUCTOS_ACTIVOS")
    resultado = cursor.fetchall()
    workbook = xlsxwriter.Workbook(output)
    hoja = workbook.add_worksheet("Inventario")

    estilo_cuerpo = workbook.add_format({
        'font_name': 'Arial',
        'border': 1
    })
    estilo_cuerpo.set_align('center')
    estilo_cuerpo.set_align('vcenter')

    # estilo encabezado
    titulo = workbook.add_format({
        'bold': True,
        'font_color': 'green',
        'font_size': 18,
        'border': 1,
    })
    titulo.set_align('center')
    titulo.set_align('vcenter')

    hoja.merge_range('A1:B4', "", estilo_cuerpo)
    hoja.merge_range('C1:I2', "Fluidos McGreen de México S.A de C.V", titulo)
    hoja.merge_range('C3:I4', "Inventario general", titulo)
    hoja.write(0, 9, "Código:", estilo_cuerpo)
    hoja.write(1, 9, "Revisión:", estilo_cuerpo)
    hoja.merge_range('J3:J4', "Fecha de revisión:", estilo_cuerpo)
    hoja.write(0, 10, "MG-FO-ADM-005", estilo_cuerpo)
    hoja.write(1, 10, "00", estilo_cuerpo)
    hoja.merge_range('K3:K4', "01-02-2022", estilo_cuerpo)
    # fin

    # campos del encabezado de la tabla
    hoja.write(4, 0, "Identificador", estilo_cuerpo)
    hoja.write(4, 1, "Nombre", estilo_cuerpo)
    hoja.write(4, 2, "Descripción", estilo_cuerpo)
    hoja.write(4, 3, "Cantidad", estilo_cuerpo)
    hoja.write(4, 4, "Medida", estilo_cuerpo)
    hoja.write(4, 5, "Departamento", estilo_cuerpo)
    hoja.write(4, 6, "Precio unitario", estilo_cuerpo)
    hoja.write(4, 7, "Subtotal", estilo_cuerpo)
    hoja.write(4, 8, "Precio total", estilo_cuerpo)
    hoja.write(4, 9, "Tipo de cambio", estilo_cuerpo)
    hoja.write(4, 10, "Sucursal", estilo_cuerpo)
    # fin
    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 11):
            hoja.write(fila, col, u'%s' % resultado[row - 1][col], estilo_cuerpo)
        fila = 1 + fila

    workbook.close()
    output.seek(0)
    filename = 'Inventario.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def exportar_compras_xls(request):
    fecha_hoy = datetime.datetime.now()
    hoy = str(fecha_hoy.month) + "-" + str(fecha_hoy.day) + "-" + str(fecha_hoy.year)
    cursor = connection.cursor()
    cursor.callproc("MOSTRAR_COMPRAS")
    resultado = cursor.fetchall()
    workbook = xlwt.Workbook()
    hoja_1 = workbook.add_sheet('Inventario', cell_overwrite_ok=True)
    font_encabezado = xlwt.Font()
    font_cuerpo = xlwt.Font()
    
    font_encabezado.name = 'Arial'
    font_encabezado.bold = True
    font_encabezado.height = 10 * 10
    font_cuerpo.name = 'Arial'
    font_encabezado.height = 15 * 15

    estilo_encabezado = xlwt.XFStyle()
    estilo_cuerpo = xlwt.XFStyle()
    estilo_encabezado.font = font_encabezado
    estilo_cuerpo.font = font_cuerpo
    bordes = xlwt.Borders()
    bordes.left = 1
    bordes.right = 1
    bordes.top = 1
    bordes.bottom = 1
    estilo_encabezado.borders = bordes
    estilo_cuerpo.borders = bordes

    # comienzo Estilos celdas de encabezado
    imagen = xlwt.Borders()
    imagen.left = 1
    imagen.right = 1
    imagen.top = 1
    imagen.bottom = 1
    titulo = xlwt.Font()
    titulo_xfs = xlwt.XFStyle()
    titulo_alineado = xlwt.Alignment()
    titulo_alineado.horz = xlwt.Alignment.HORZ_CENTER
    titulo_alineado.vert = xlwt.Alignment.VERT_CENTER
    titulo.name = 'Arial'
    titulo.bold = True
    titulo.height = 18 * 18
    titulo.colour_index = xlwt.Style.colour_map["green"]
    titulo_xfs.font = titulo
    titulo_xfs.borders = bordes
    titulo_xfs.alignment = titulo_alineado
    pagina = xlwt.Font()
    pagina_xfs = xlwt.XFStyle()
    pagina.name = 'Arial'
    pagina.bold = True
    pagina.height = 15 * 15
    pagina_xfs.colour_index = xlwt.Style.colour_map["black"]
    pagina_xfs.font = pagina
    pagina_xfs.borders = bordes
    pagina_xfs.alignment = titulo_alineado
    estilo_encabezado.alignment = titulo_alineado

    border_celdas_vacias = xlwt.Borders()
    border_celdas_vacias_xfs = xlwt.XFStyle()
    border_celdas_vacias.left = 1
    border_celdas_vacias.right = 1
    border_celdas_vacias.top = 1
    border_celdas_vacias.bottom = 1
    border_celdas_vacias_xfs.borders = border_celdas_vacias
    border_celdas_vacias_pagina = xlwt.Borders()
    border_celdas_vacias_pagina_xfs = xlwt.XFStyle()
    border_celdas_vacias_pagina.left = 1
    border_celdas_vacias_pagina.right = 1
    border_celdas_vacias_pagina.top = 1
    border_celdas_vacias_pagina.bottom = 1
    border_celdas_vacias_pagina_xfs.borders = border_celdas_vacias

    hoja_1.write_merge(0, 3, 0, 1, "", titulo_xfs)
    hoja_1.write_merge(0, 1, 2, 6, "Fluidos McGreen de México S.A de C.V", titulo_xfs)
    hoja_1.write_merge(2, 3, 2, 6, "COMPRAS REALIZADAS", titulo_xfs)
    hoja_1.write(0, 7, "Código:", estilo_encabezado)
    hoja_1.write(1, 7, "Revisión:", estilo_encabezado)
    hoja_1.write_merge(2, 3, 7, 7, "Fecha de revisión:", pagina_xfs)
    hoja_1.write(0, 8, "MG-FO-ADM-005", border_celdas_vacias_xfs)
    hoja_1.write(1, 8, "00", border_celdas_vacias_xfs)
    hoja_1.write_merge(2, 3, 8, 8, "01-02-2022", border_celdas_vacias_pagina_xfs)
    # fin

    # encabezado de tabla
    hoja_1.write(4, 0, "Compra", estilo_encabezado)
    hoja_1.write(4, 1, "Detalle", estilo_encabezado)
    hoja_1.write(4, 2, "RFC", estilo_encabezado)
    hoja_1.write(4, 3, "Proveedor", estilo_encabezado)
    hoja_1.write(4, 4, "Nombre de producto", estilo_encabezado)
    hoja_1.write(4, 5, "Cantidad", estilo_encabezado)
    hoja_1.write(4, 6, "Precio unitario", estilo_encabezado)
    hoja_1.write(4, 7, "Medida", estilo_encabezado)
    hoja_1.write(4, 8, "Precio total", estilo_encabezado)
    # fin

    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 9):
            hoja_1.write(fila, col, u'%s' % resultado[row - 1][col], estilo_cuerpo)
        fila = 1 + fila
    nombre_archivo ="Compras.xls"
    response = HttpResponse(content_type="application/Excel") 
    contenido = "attachment; filename={0}".format(nombre_archivo)
    response["Content-Disposition"] = contenido
    response["ContentType"] = "application/vnd.ms-excel"
    workbook.save(response)
    cursor.close()
    return response

def exportar_compras_xlsx(request):
    fecha_hoy = datetime.datetime.now()
    hoy = str(fecha_hoy.month) + "-" + str(fecha_hoy.day) + "-" + str(fecha_hoy.year)
    output = io.BytesIO()
    cursor = connection.cursor()
    cursor.callproc("MOSTRAR_COMPRAS")
    resultado = cursor.fetchall()
    workbook = xlsxwriter.Workbook(output)
    hoja = workbook.add_worksheet("Compras")

    estilo_cuerpo = workbook.add_format({
        'font_name': 'Arial',
        'border': 1
    })
    estilo_cuerpo.set_align('center')
    estilo_cuerpo.set_align('vcenter')

    # estilo encabezado
    titulo = workbook.add_format({
        'bold': True,
        'font_color': 'green',
        'font_size': 18,
        'border': 1,
    })
    titulo.set_align('center')
    titulo.set_align('vcenter')
    
    hoja.merge_range('A1:B4', "", estilo_cuerpo)
    hoja.merge_range('C1:G2', "Fluidos McGreen de México S.A de C.V", titulo)
    hoja.merge_range('C3:G4', "COMPRAS REALIZADAS", titulo)
    hoja.write(0, 7, "Código:", estilo_cuerpo)
    hoja.write(1, 7, "Revisión:", estilo_cuerpo)
    hoja.merge_range('H3:H4', "Fecha de revisión:", estilo_cuerpo)
    hoja.write(0, 8, "MG-FO-ADM-005", estilo_cuerpo)
    hoja.write(1, 8, "00", estilo_cuerpo)
    hoja.merge_range('I3:I4', "01-02-2022", estilo_cuerpo)
    # fin

    # campos del encabezado de la tabla
    hoja.write(4, 0, "Compra", estilo_cuerpo)
    hoja.write(4, 1, "Detalle", estilo_cuerpo)
    hoja.write(4, 2, "RFC", estilo_cuerpo)
    hoja.write(4, 3, "Proveedor", estilo_cuerpo)
    hoja.write(4, 4, "Nombre de producto", estilo_cuerpo)
    hoja.write(4, 5, "Cantidad", estilo_cuerpo)
    hoja.write(4, 6, "Precio unitario", estilo_cuerpo)
    hoja.write(4, 7, "Medida", estilo_cuerpo)
    hoja.write(4, 8, "Precio total", estilo_cuerpo)
    # fin
    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 9):
            hoja.write(fila, col, u'%s' % resultado[row - 1][col], estilo_cuerpo)
        fila = 1 + fila

    workbook.close()
    output.seek(0)
    filename = 'Compras.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def exportar_ventas_xls(request):
    fecha_hoy = datetime.datetime.now()
    hoy = str(fecha_hoy.month) + "-" + str(fecha_hoy.day) + "-" + str(fecha_hoy.year)
    cursor = connection.cursor()
    cursor.callproc("MOSTRAR_VENTAS_MOD")
    resultados = cursor.fetchall()

    libro = xlwt.Workbook("")
    hoja_1 = libro.add_sheet("Ventas")
    
    font_encabezado = xlwt.Font()
    font_cuerpo = xlwt.Font() 
    font_encabezado.name = 'Arial'
    font_encabezado.bold = True
    font_encabezado.height = 10 * 10
    font_cuerpo.name = 'Arial'
    font_encabezado.height = 15 * 15

    estilo_encabezado = xlwt.XFStyle()
    estilo_cuerpo = xlwt.XFStyle()
    estilo_encabezado.font = font_encabezado
    estilo_cuerpo.font = font_cuerpo
    bordes = xlwt.Borders()
    bordes.left = 1
    bordes.right = 1
    bordes.top = 1
    bordes.bottom = 1
    estilo_encabezado.borders = bordes
    estilo_cuerpo.borders = bordes

    # comienzo Estilos celdas de encabezado
    imagen = xlwt.Borders()
    imagen.left = 1
    imagen.right = 1
    imagen.top = 1
    imagen.bottom = 1
    titulo = xlwt.Font()
    titulo_xfs = xlwt.XFStyle()
    titulo_alineado = xlwt.Alignment()
    titulo_alineado.horz = xlwt.Alignment.HORZ_CENTER
    titulo_alineado.vert = xlwt.Alignment.VERT_CENTER
    titulo.name = 'Arial'
    titulo.bold = True
    titulo.height = 18 * 18
    titulo.colour_index = xlwt.Style.colour_map["green"]
    titulo_xfs.font = titulo
    titulo_xfs.borders = bordes
    titulo_xfs.alignment = titulo_alineado
    pagina = xlwt.Font()
    pagina_xfs = xlwt.XFStyle()
    pagina.name = 'Arial'
    pagina.bold = True
    pagina.height = 15 * 15
    pagina_xfs.colour_index = xlwt.Style.colour_map["black"]
    pagina_xfs.font = pagina
    pagina_xfs.borders = bordes
    pagina_xfs.alignment = titulo_alineado
    estilo_encabezado.alignment = titulo_alineado

    border_celdas_vacias = xlwt.Borders()
    border_celdas_vacias_xfs = xlwt.XFStyle()
    border_celdas_vacias.left = 1
    border_celdas_vacias.right = 1
    border_celdas_vacias.top = 1
    border_celdas_vacias.bottom = 1
    border_celdas_vacias_xfs.borders = border_celdas_vacias
    border_celdas_vacias_pagina = xlwt.Borders()
    border_celdas_vacias_pagina_xfs = xlwt.XFStyle()
    border_celdas_vacias_pagina.left = 1
    border_celdas_vacias_pagina.right = 1
    border_celdas_vacias_pagina.top = 1
    border_celdas_vacias_pagina.bottom = 1
    border_celdas_vacias_pagina_xfs.borders = border_celdas_vacias

    hoja_1.write_merge(0, 3, 0, 1, "", titulo_xfs)
    hoja_1.write_merge(0, 1, 2, 6, "Fluidos McGreen de México S.A de C.V", titulo_xfs)
    hoja_1.write_merge(2, 3, 2, 6, "CUENTAS POR COBRAR", titulo_xfs)
    hoja_1.write(0, 7, "Código:", estilo_encabezado)
    hoja_1.write(1, 7, "Revisión:", estilo_encabezado)
    hoja_1.write_merge(2, 3, 7, 7, "Fecha de revisión:", pagina_xfs)
    hoja_1.write(0, 8, "MG-FO-ADM-003", border_celdas_vacias_xfs)
    hoja_1.write(1, 8, "00", border_celdas_vacias_xfs)
    hoja_1.write_merge(2, 3, 8, 8, "01-11-2021", border_celdas_vacias_pagina_xfs)
    # fin

    # encabezado de tabla
    hoja_1.write(4, 0, "Venta", estilo_encabezado)
    hoja_1.write(4, 1, "Status", estilo_encabezado)
    hoja_1.write(4, 2, "Fecha de pago de factura", estilo_encabezado)
    hoja_1.write(4, 3, "Contrarecibo", estilo_encabezado)
    hoja_1.write(4, 4, "Fecha de recibo de pago", estilo_encabezado)
    hoja_1.write(4, 5, "SP", estilo_encabezado)
    hoja_1.write(4, 6, "OC", estilo_encabezado)
    hoja_1.write(4, 7, "Fecha", estilo_encabezado)
    hoja_1.write(4, 8, "Producto", estilo_encabezado)
    hoja_1.write(4, 9, "Medida", estilo_encabezado)
    hoja_1.write(4, 10, "Pozo", estilo_encabezado)
    hoja_1.write(4, 11, "Total servicios", estilo_encabezado)
    hoja_1.write(4, 12, "Precio unitario", estilo_encabezado)
    hoja_1.write(4, 13, "Subtotal USD", estilo_encabezado)
    hoja_1.write(4, 14, "IVA", estilo_encabezado)
    hoja_1.write(4, 15, "Total USD por servicio", estilo_encabezado)
    hoja_1.write(4, 16, "Monto total", estilo_encabezado)
    hoja_1.write(4, 17, "Num. factura", estilo_encabezado)
    hoja_1.write(4, 18, "Fecha de factura", estilo_encabezado)
    hoja_1.write(4, 19, "Recibo de pago de factura McGreen", estilo_encabezado)
    hoja_1.write(4, 20, "Fecha de recibo de pago", estilo_encabezado)
    hoja_1.write(4, 21, "Dólar", estilo_encabezado)
    hoja_1.write(4, 22, "Monto MXP", estilo_encabezado)
    hoja_1.write(4, 23, "Monto MXP pagado", estilo_encabezado)
    # fin

    fila_comienzo = 5

    for fila_dato in range(1, len(resultados) + 1):
        for columna in range(0, 24):
            hoja_1.write(fila_comienzo, columna, u'%s' % resultados[fila_dato - 1][columna], estilo_cuerpo)
        fila_comienzo = fila_comienzo + 1
    
    nombre_archivo = "Cuentas por cobrar.xls"
    response = HttpResponse(content_type="application/Excel")
    contenido = "attachmen; filename={0}".format(nombre_archivo)
    response["Content-Disposition"] = contenido
    response["Content-Type"] = "application/vnd.ms-excel"
    libro.save(response)
    cursor.close()
    return response

def exportar_ventas_xlsx(request):
    fecha_hoy = datetime.datetime.now()
    hoy = str(fecha_hoy.month) + "-" + str(fecha_hoy.day) + "-" + str(fecha_hoy.year)
    output = io.BytesIO()
    cursor = connection.cursor()
    cursor.callproc("MOSTRAR_VENTAS_MOD")
    resultado = cursor.fetchall()
    workbook = xlsxwriter.Workbook(output)
    hoja = workbook.add_worksheet("Ventas")

    estilo_cuerpo = workbook.add_format({
        'font_name': 'Arial',
        'border': 1
    })
    estilo_cuerpo.set_align('center')
    estilo_cuerpo.set_align('vcenter')

    # estilo encabezado
    titulo = workbook.add_format({
        'bold': True,
        'font_color': 'green',
        'font_size': 18,
        'border': 1,
    })
    titulo.set_align('center')
    titulo.set_align('vcenter')

    hoja.merge_range('A1:B4', "", estilo_cuerpo)
    hoja.merge_range('C1:G2', "Fluidos McGreen de México S.A de C.V", titulo)
    hoja.merge_range('C3:G4', "CUENTAS POR COBRAR", titulo)
    hoja.write(0, 7, "Código:", estilo_cuerpo)
    hoja.write(1, 7, "Revisión:", estilo_cuerpo)
    hoja.merge_range('H3:H4', "Fecha de revisión:", estilo_cuerpo)
    hoja.write(0, 8, "MG-FO-ADM-003", estilo_cuerpo)
    hoja.write(1, 8, "00", estilo_cuerpo)
    hoja.merge_range('I3:I4', "01-11-2021", estilo_cuerpo)
    # fin

    # encabezado de tabla
    hoja.write(4, 0, "Venta", estilo_cuerpo)
    hoja.write(4, 1, "Status", estilo_cuerpo)
    hoja.write(4, 2, "Fecha de pago de factura", estilo_cuerpo)
    hoja.write(4, 3, "Contrarecibo", estilo_cuerpo)
    hoja.write(4, 4, "Fecha de recibo de pago", estilo_cuerpo)
    hoja.write(4, 5, "SP", estilo_cuerpo)
    hoja.write(4, 6, "OC", estilo_cuerpo)
    hoja.write(4, 7, "Fecha", estilo_cuerpo)
    hoja.write(4, 8, "Producto", estilo_cuerpo)
    hoja.write(4, 9, "Medida", estilo_cuerpo)
    hoja.write(4, 10, "Pozo", estilo_cuerpo)
    hoja.write(4, 11, "Total servicios", estilo_cuerpo)
    hoja.write(4, 12, "Precio unitario", estilo_cuerpo)
    hoja.write(4, 13, "Subtotal USD", estilo_cuerpo)
    hoja.write(4, 14, "IVA", estilo_cuerpo)
    hoja.write(4, 15, "Total USD por servicio", estilo_cuerpo)
    hoja.write(4, 16, "Monto total", estilo_cuerpo)
    hoja.write(4, 17, "Num. factura", estilo_cuerpo)
    hoja.write(4, 18, "Fecha de factura", estilo_cuerpo)
    hoja.write(4, 19, "Recibo de pago de factura McGreen", estilo_cuerpo)
    hoja.write(4, 20, "Fecha de recibo de pago", estilo_cuerpo)
    hoja.write(4, 21, "Dólar", estilo_cuerpo)
    hoja.write(4, 22, "Monto MXP", estilo_cuerpo)
    hoja.write(4, 23, "Monto MXP pagado", estilo_cuerpo)
    # fin
    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 24):
            hoja.write(fila, col, u'%s' % resultado[row - 1][col], estilo_cuerpo)
        fila = 1 + fila

    workbook.close()
    output.seek(0)
    filename = 'Cuentas por cobrar.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def exportar_diferentes_movimientos_xls(request):
    fecha_hoy = datetime.datetime.now()
    hoy = str(fecha_hoy.month) + "-" + str(fecha_hoy.day) + "-" + str(fecha_hoy.year)
    cursor = connection.cursor()
    cursor.callproc("MOSTRAR_MOV_IND")
    resultado = cursor.fetchall()
    workbook = xlwt.Workbook()
    hoja_1 = workbook.add_sheet('Movimientos', cell_overwrite_ok=True)
    font_encabezado = xlwt.Font()
    font_cuerpo = xlwt.Font()
    
    font_encabezado.name = 'Arial'
    font_encabezado.bold = True
    font_encabezado.height = 10 * 10
    font_cuerpo.name = 'Arial'
    font_encabezado.height = 15 * 15

    estilo_encabezado = xlwt.XFStyle()
    estilo_cuerpo = xlwt.XFStyle()
    estilo_encabezado.font = font_encabezado
    estilo_cuerpo.font = font_cuerpo
    bordes = xlwt.Borders()
    bordes.left = 1
    bordes.right = 1
    bordes.top = 1
    bordes.bottom = 1
    estilo_encabezado.borders = bordes
    estilo_cuerpo.borders = bordes

    # comienzo Estilos celdas de encabezado
    imagen = xlwt.Borders()
    imagen.left = 1
    imagen.right = 1
    imagen.top = 1
    imagen.bottom = 1
    titulo = xlwt.Font()
    titulo_xfs = xlwt.XFStyle()
    titulo_alineado = xlwt.Alignment()
    titulo_alineado.horz = xlwt.Alignment.HORZ_CENTER
    titulo_alineado.vert = xlwt.Alignment.VERT_CENTER
    titulo.name = 'Arial'
    titulo.bold = True
    titulo.height = 18 * 18
    titulo.colour_index = xlwt.Style.colour_map["green"]
    titulo_xfs.font = titulo
    titulo_xfs.borders = bordes
    titulo_xfs.alignment = titulo_alineado
    pagina = xlwt.Font()
    pagina_xfs = xlwt.XFStyle()
    pagina.name = 'Arial'
    pagina.bold = True
    pagina.height = 15 * 15
    pagina_xfs.colour_index = xlwt.Style.colour_map["black"]
    pagina_xfs.font = pagina
    pagina_xfs.borders = bordes
    pagina_xfs.alignment = titulo_alineado
    estilo_encabezado.alignment = titulo_alineado

    border_celdas_vacias = xlwt.Borders()
    border_celdas_vacias_xfs = xlwt.XFStyle()
    border_celdas_vacias.left = 1
    border_celdas_vacias.right = 1
    border_celdas_vacias.top = 1
    border_celdas_vacias.bottom = 1
    border_celdas_vacias_xfs.borders = border_celdas_vacias
    border_celdas_vacias_pagina = xlwt.Borders()
    border_celdas_vacias_pagina_xfs = xlwt.XFStyle()
    border_celdas_vacias_pagina.left = 1
    border_celdas_vacias_pagina.right = 1
    border_celdas_vacias_pagina.top = 1
    border_celdas_vacias_pagina.bottom = 1
    border_celdas_vacias_pagina_xfs.borders = border_celdas_vacias

    hoja_1.write_merge(0, 3, 0, 1, "", titulo_xfs)
    hoja_1.write_merge(0, 1, 2, 6, "Fluidos McGreen de México S.A de C.V", titulo_xfs)
    hoja_1.write_merge(2, 3, 2, 6, "MOVIMIENTOS REALIZADOS", titulo_xfs)
    hoja_1.write(0, 7, "Código:", estilo_encabezado)
    hoja_1.write(1, 7, "Revisión:", estilo_encabezado)
    hoja_1.write_merge(2, 3, 7, 7, "Fecha de revisión:", pagina_xfs)
    hoja_1.write(0, 8, "", border_celdas_vacias_xfs)
    hoja_1.write(1, 8, "00", border_celdas_vacias_xfs)
    hoja_1.write_merge(2, 3, 8, 8, hoy, border_celdas_vacias_pagina_xfs)
    # fin

    # encabezado de tabla
    hoja_1.write(4, 0, "Movimiento", estilo_encabezado)
    hoja_1.write(4, 1, "Tipo de movimiento", estilo_encabezado)
    hoja_1.write(4, 2, "Producto", estilo_encabezado)
    hoja_1.write(4, 3, "Fecha", estilo_encabezado)
    hoja_1.write(4, 4, "Origen o destino", estilo_encabezado)
    hoja_1.write(4, 5, "Departamento", estilo_encabezado)
    hoja_1.write(4, 6, "Motivo", estilo_encabezado)
    hoja_1.write(4, 7, "Cantidad", estilo_encabezado)
    hoja_1.write(4, 8, "Medida", estilo_encabezado)
    # fin

    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 9):
            hoja_1.write(fila, col, u'%s' % resultado[row - 1][col], estilo_cuerpo)
        fila = 1 + fila
    nombre_archivo ="Movimientos.xls"
    response = HttpResponse(content_type="application/Excel") 
    contenido = "attachment; filename={0}".format(nombre_archivo)
    response["Content-Disposition"] = contenido
    response["ContentType"] = "application/vnd.ms-excel"
    workbook.save(response)
    cursor.close()
    return response

def exportar_diferentes_movimientos_xlsx(request):
    fecha_hoy = datetime.datetime.now()
    hoy = str(fecha_hoy.month) + "-" + str(fecha_hoy.day) + "-" + str(fecha_hoy.year)
    output = io.BytesIO()
    cursor = connection.cursor()
    cursor.callproc("MOSTRAR_MOV_IND")
    resultado = cursor.fetchall()
    workbook = xlsxwriter.Workbook(output)
    hoja = workbook.add_worksheet("Compras")

    estilo_cuerpo = workbook.add_format({
        'font_name': 'Arial',
        'border': 1
    })
    estilo_cuerpo.set_align('center')
    estilo_cuerpo.set_align('vcenter')

    # estilo encabezado
    titulo = workbook.add_format({
        'bold': True,
        'font_color': 'green',
        'font_size': 18,
        'border': 1,
    })
    titulo.set_align('center')
    titulo.set_align('vcenter')

    hoja.merge_range('A1:B4', "", estilo_cuerpo)
    hoja.merge_range('C1:G2', "Fluidos McGreen de México S.A de C.V", titulo)
    hoja.merge_range('C3:G4', "MOVIMIENTOS REALIZADOS", titulo)
    hoja.write(0, 7, "Código:", estilo_cuerpo)
    hoja.write(1, 7, "Revisión:", estilo_cuerpo)
    hoja.merge_range('H3:H4', "Fecha de revisión:", estilo_cuerpo)
    hoja.write(0, 8, "", estilo_cuerpo)
    hoja.write(1, 8, "00", estilo_cuerpo)
    hoja.merge_range('I3:I4', hoy, estilo_cuerpo)
    # fin

    # campos del encabezado de la tabla
    hoja.write(4, 0, "Movimiento", estilo_cuerpo)
    hoja.write(4, 1, "Tipo de movimiento", estilo_cuerpo)
    hoja.write(4, 2, "Producto", estilo_cuerpo)
    hoja.write(4, 3, "Fecha", estilo_cuerpo)
    hoja.write(4, 4, "Origen o destino",estilo_cuerpo)
    hoja.write(4, 5, "Departamento", estilo_cuerpo)
    hoja.write(4, 6, "Motivo", estilo_cuerpo)
    hoja.write(4, 7, "Cantidad", estilo_cuerpo)
    hoja.write(4, 8, "Medida", estilo_cuerpo)
    # fin
    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 9):
            hoja.write(fila, col, u'%s' % resultado[row - 1][col], estilo_cuerpo)
        fila = 1 + fila

    workbook.close()
    output.seek(0)
    filename = 'Movimientos.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
