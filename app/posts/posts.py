import io
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from .. import models
from django.db import connection
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
                cursor = connection.cursor()
                ext_email = formulario["slemail"].value()
                cursor.callproc("AGREGAR_USUARIO",[request.session.get("email"), formulario["matricula"].value(),formulario["nombre_usuario"].value(),formulario["ap_p"].value(),formulario["ap_m"].value(),formulario["sl_puestos"].value(),formulario["email"].value()+ext_email,formulario["contra"].value(),formulario["rol"].value()])
                mensaje = cursor.fetchall()[0][0]
                print(mensaje)
                if mensaje != 'USUARIO CREADO':
                    messages.error(request, mensaje)
                else:
                    messages.success(request, "El usuario ha sido creado éxitosamente")
                cursor.close()
                return redirect("/Registro")
            else:
                print(formulario.errors)
                return HttpResponse("Debe llenar los campos de manera correcta")
        return HttpResponse("No hice nada")

def agregar_producto(request):
    if request.session.get('email'):
        if request.method == 'POST':
            if request.POST.get("producto") is not None and request.POST.get("descripcion") is not None and request.POST.get("cantidad") is not None and request.POST.get("ddw_medidas") is not None and request.POST.get("ddw_departamentos") is not None and request.POST.get("precio") is not None and request.POST.get("sl_tipo_cambio") is not None and request.POST.get("sucursal") is not None and request.session.get("email") is not None:
                try:
                    cursor = connection.cursor()
                    cursor.callproc("Agrega_INV", [request.POST["producto"], request.POST["descripcion"], request.POST["cantidad"], request.POST["ddw_medidas"], request.POST["ddw_departamentos"], request.POST["precio"], request.POST["sl_tipo_cambio"], request.POST["sucursal"], request.session.get("email")])
                    if cursor.fetchall()[0][0] != 'FACTURA DISPONIBLE':
                        messages.error(request, "Ocurrió un error al hacer la modificación")
                    messages.success(request, "Producto registrado con éxito")
                finally:
                    cursor.close()
            else:
                messages.error(request, "Debe llenar todos los campos")
            return redirect("/Inventario_general")

def modificar_producto(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.callproc("MODIFICA_INV", [request.session.get('email'), request.POST["id_producto"], request.POST["producto"], request.POST["descripcion"], request.POST["precio"]])
        if cursor.fetchall()[0][0] != 'EL PRECIO FUE MODIFICADO CORRECTAMENTE':
            messages.error(request, "Ocurrió un error al hacer la modificación")
        messages.success(request, "Elementos actualizados con éxito")
        return redirect("/Inventario_general")

def descontinuar_producto(request,id_prod):
    if request.session.get("email"):
        cursor = connection.cursor()
        cursor.callproc("DESCONTINUAR_PRODUCTO", [id_prod, request.session.get("email")])
        if cursor.fetchall()[0][0] != 'EL PRODUCTO: ' + id_prod + ' FUE DESCONTINUADO':
            messages.error(request, "Ocurrió un error al eliminar el producto")
        messages.error(request, "Producto eliminado")
        cursor.close()
        return redirect("/Inventario_general")
    else:
        return redirect("/cerrar_sesion")

def activar_producto(request,id_prod):
    if request.session.get("email"):
        cursor = connection.cursor()
        cursor.callproc("ACTIVAR_PRODUCTO", [request.session.get('email'), id_prod])
        if cursor.fetchall()[0][0] != 'EL PRODUCTO: ' + id_prod + ' FUE ACTIVADO':
            messages.error(request, "Ocurrió un error al activar el producto")
        messages.success(request, "Producto activado")
        cursor.close()
        return redirect("/Inventario_general")
    else:
        return redirect("/cerrar_sesion")

def generar_compra(request):
    if request.session.get('email'):
        if request.method == 'POST':
            cursor = connection.cursor()
            cursor.callproc("COMPRA",[request.POST["sl_productos"], request.POST["comprador"], request.POST["cantidad"], request.POST["p_u"], request.POST["fecha_compra"], request.POST["sl_proveedores"], request.POST["motivo"]])
            mensaje = cursor.fetchall()
            print(mensaje)
            # if mensaje != 'FACTURA DISPONIBLE':
            #     messages.error(request, "Ocurrió un error al realizar la compra")
            # else:
            #     messages.success(request, "Compra registrada")
            cursor.close()
            return redirect("/Compras")
    else:
        return redirect("/cerrar_sesion")

def generar_venta(request):
    if request.session.get('email'):
        if request.method == 'POST':
            cursor = connection.cursor()
            cursor.callproc("VENTA_MOD",[request.POST["sl_sistemas"].split(' ')[0],request.POST["vendedor"],request.POST["cantidad"],request.POST["p_u"],request.POST["fecha"],request.POST["motivo"],request.POST["sl_clientes"],request.POST["articulo"]])
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
            cursor = connection.cursor()
            sistema = str(request.POST['sl_sistemas']).split(' ')[0]
            if request.POST.get("sp") is not None and request.POST.get("oc") is not None and request.POST.get("fecha") is not None and sistema is not None and request.POST.get("pozo") is not None and request.POST.get("total_servicios") is not None and request.POST.get("no_factura") is not None and request.POST.get("dolares") is not None and request.POST.get("monto_mp_pagado") is not None:
                cursor.callproc("VENTA_MOD",[request.POST['email'],request.POST['status'],request.POST['fecha_pago_fac'],request.POST['contrarecibo'],request.POST['fecha_rec_pago'],request.POST['sp'],request.POST['oc'],request.POST['fecha'],sistema,request.POST['pozo'],request.POST['total_servicios'],request.POST['no_factura'],request.POST['fecha_de_fac'],request.POST['recibo_pago_fac_mcgreen'],request.POST['fecha_r_pag'],request.POST['dolares'],request.POST['monto_mp_pagado']])
                mensaje = cursor.fetchone()[0]
                print(mensaje)
                if mensaje != 'CUENTA POR COBRAR AGREGADA CORRECTAMENTE VERIFIQUE LOS MOVIMIENTOS':
                    messages.error(request, "Ocurrió un error al realizar la venta")
                else:
                    messages.success(request, "Venta registrada")
            else:
                messages.error(request, "Debe llenar los campos requeridos")
            cursor.close()
            return redirect("/Ventas")
        else:
            return redirect("/Ventas")
    else:
        return redirect("/cerrar_sesion")

def modificar_cuenta_por_cobrar(request):
    if request.session.get('email'):
        if request.method == 'POST':
            cursor = connection.cursor()
            cursor.callproc("MODIFICA_VENTA_MOD",[request.POST["id_"], request.POST["email"], request.POST["status"], request.POST["fecha_pago_fac"], request.POST["contrarecibo"], request.POST["fecha_rec_pago"], request.POST["fecha_de_fac"], request.POST["recibo_pago_fac_mcgreen"], request.POST["fecha_r_pag"], request.POST["monto_mn_pagado"]])
            if cursor.fetchall()[0][0] != "CUENTA POR COBRAR MODIFICADA CORRECTAMENTE":
                messages.error(request, "No se pudo realizar la modificación")
            else:
                messages.success(request, "Cuenta por cobrar modificada correctamente")
            cursor.close()
            return redirect("/Ver_cuentas_por_cobrar")
        return redirect("/Ver_cuentas_por_cobrar")
    return redirect("/cerrar_sesion")
    

def agregar_otros(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.callproc("MOV_INV", [request.POST["sl_productos"], request.POST["email"], request.POST["cantidad"], request.POST["fecha_otro"], request.POST["motivo"], request.POST["sl_tipo_mov"], request.POST["org_des"]])
        if cursor.fetchall()[0][0] != 'FACTURA DISPONIBLE':
            messages.error(request, "Ocurrió un error al realizar la operación")
        else:
            messages.success(request, "Operación realizada correctamente")
        cursor.close()
        return redirect("/Otras_E_S")

def conseguir_precio(request,prod):
    if request.is_ajax():
        precios = models.PRECIO_INV_VENTA.objects.filter(ID_PRODUCTO_id=prod).values_list("PRECIO_UNIT_VENTA")[0][0]
        return JsonResponse({'data': precios})
    return HttpResponse("Wrong request")

# Proveedores
def agregar_proveedores(request):
    if request.session.get('email'):
        if request.method == 'POST':
            form = formulario_proveedor(request.POST)
            if form.is_valid():
                cursor = connection.cursor()
                cursor.callproc("Agrega_Proveedor",[request.session.get('email'), form["Identificador"].value(),form["proveedor"].value(),form["telefono"].value(),form["email"].value()])
                cursor.close()
                return redirect("/Compras")    
        return redirect("/Compras")
    else:
        return redirect("/cerrar_sesion")

def agregar_clientes(request):
    if request.session.get('email'):
        if request.method == 'POST':
            form = formulario_cliente(request.POST)
            if request.POST.get("Identificador") is not None and request.POST.get("cliente") is not None and request.POST.get("direccion") is not None and request.POST.get("telefono") is not None and request.POST.get("email") is not None:
                if form.is_valid():
                    cursor = connection.cursor()
                    cursor.callproc("Agrega_CLIENTE",[form["Identificador"].value(), form["cliente"].value(), form["direccion"].value(), form["telefono"].value(), form["email"].value()])
                    mensaje = cursor.fetchall()[0][0]
                    if mensaje == 'Cliente insertado correctamente':
                        messages.success(request, "Nuevo cliente agregado")
                    else:
                        messages.error(request, "No se pudo agregar el cliente")
                    cursor.close()
                else:
                    messages.error(request, "Debe llenar los campos con la información que se le pide")
            else:
                messages.error(request, "Debe llenar todos los campos")
                return redirect("/Ventas")    
        return redirect("/Ventas")
    else:
        return redirect("/cerrar_sesion")

# def exportar_inventario_excel(request):
#     cursor = connection.cursor()
#     cursor.callproc("MOSTRAR_PRODUCTOS_ACTIVOS")
#     filas_datos = cursor.fetchall()
#     cont = 0
#     cont = [cont + 1 for row in filas_datos]
    
#     bordes = Border(left=Side(border_style=BORDER_THIN), top=Side(border_style=BORDER_THIN), right=Side(border_style=BORDER_THIN), bottom=Side(border_style=BORDER_THIN))

#     wb = Workbook()
#     ws = wb.active
#     ws.merge_cells('A1:B4')
#     fila_A1 = ws['A1']
#     fila_A1.border = bordes

#     filas_C1_G4 = ws['C1:G4']
#     for fila in filas_C1_G4:
#         fila[0].border = bordes

#     ws['C1'] = 'PRODUCTOS EXISTENTES'
#     ws.merge_cells('C1:G4')
    fila_C1 = ws['C1']
    fila_C1.font = Font(bold=True, color="00008000", size=20, name="Arial")
    fila_C1.alignment = Alignment(horizontal="center", vertical="center")
    fila_C1.border = bordes
    
#     ws['H1'] = 'Código:'
#     fila_H1 = ws['H1']
#     fila_H1.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_H1.alignment = Alignment(horizontal="left", vertical="center")
#     fila_H1.border = bordes
#     fila_I1 = ws['I1']
#     fila_I1.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_I1.alignment = Alignment(horizontal="left", vertical="center")
#     fila_I1.border = bordes
    
#     ws['H2'] = 'Revisión:'
#     fila_H2 = ws['H2']
#     fila_H2.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_H2.alignment = Alignment(horizontal="left", vertical="center")
#     fila_H2.border = bordes
#     fila_I2 = ws['I2']
#     fila_I2.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_I2.alignment = Alignment(horizontal="left", vertical="center")
#     fila_I2.border = bordes
    
#     filas_H3_H4 = ws['H3:H4']
#     for fila in filas_H3_H4:
#         fila[0].border = bordes
#     ws['H3'] = 'Página:'
#     ws.merge_cells('H3:H4')
#     fila_H3 = ws['H3']
#     fila_H3.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_H3.alignment = Alignment(horizontal="left", vertical="center")
#     fila_H3.border = bordes
#     filas_J3_J4 = ws['I3:J4']
#     for fila in filas_J3_J4:
#         fila[0].border = bordes
#     ws.merge_cells('I3:I4')
#     fila_H3 = ws['I3']
#     fila_H3.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_H3.alignment = Alignment(horizontal="left", vertical="center")
#     fila_H3.border = bordes



#     ws['A5'] = 'Identificador'
#     ws['A5'].font = Font(name="Arial", size=12)
#     ws['B5'] = 'Producto'
#     ws['B5'].font = Font(name="Arial", size=12)
#     ws['C5'] = 'Descripción'
#     ws['C5'].font = Font(name="Arial", size=12)
#     ws['D5'] = 'Cantidad'       
#     ws['D5'].font = Font(name="Arial", size=12)
#     ws['E5'] = 'Medida'
#     ws['E5'].font = Font(name="Arial", size=12)
#     ws['F5'] = 'Departamento'       
#     ws['F5'].font = Font(name="Arial", size=12)
#     ws['G5'] = 'Precio unitario'
#     ws['G5'].font = Font(name="Arial", size=12)
#     ws['H5'] = 'Subtotal'       
#     ws['H5'].font = Font(name="Arial", size=12)
#     ws['I5'] = 'Precio total'       
#     ws['I5'].font = Font(name="Arial", size=14)
#     filas = 6
    
#     for producto in cursor:
#         ws.cell(row=filas,column=1).value = producto[0]
#         ws.cell(row=filas,column=1).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=1).border = bordes
#         ws.cell(row=filas,column=2).value = producto[1]
#         ws.cell(row=filas,column=2).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=2).border = bordes
#         ws.cell(row=filas,column=3).value = producto[2]
#         ws.cell(row=filas,column=3).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=3).border = bordes
#         ws.cell(row=filas,column=4).value = producto[3]
#         ws.cell(row=filas,column=4).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=4).border = bordes
#         ws.cell(row=filas,column=5).value = producto[4]
#         ws.cell(row=filas,column=5).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=5).border = bordes
#         ws.cell(row=filas,column=6).value = producto[5]
#         ws.cell(row=filas,column=6).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=6).border = bordes
#         ws.cell(row=filas,column=7).value = producto[6]
#         ws.cell(row=filas,column=7).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=7).border = bordes
#         ws.cell(row=filas,column=8).value = producto[7]
#         ws.cell(row=filas,column=8).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=8).border = bordes
#         ws.cell(row=filas,column=9).value = producto[8]
#         ws.cell(row=filas,column=9).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=9).border = bordes
#         if filas != cont * 2:
#             filas = filas + 1

#     nombre_archivo ="Inventario.xlsx"
#     response = HttpResponse(content_type="application/Excel") 
#     contenido = "attachment; filename={0}".format(nombre_archivo)
#     response["Content-Disposition"] = contenido
#     wb.save(response)
#     cursor.close()
#     return response

def exportar_inventario_xls(request):
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

    hoja_1.write_merge(0, 3, 0, 1, "", titulo_xfs)
    hoja_1.write_merge(0, 3, 2, 6, "Productos existentes", titulo_xfs)
    hoja_1.write(0, 7, "Código:", estilo_encabezado)
    hoja_1.write(1, 7, "Revisión:", estilo_encabezado)
    hoja_1.write_merge(2, 3, 7, 7, "Página:", pagina_xfs)
    hoja_1.write(0, 8, "", border_celdas_vacias_xfs)
    hoja_1.write(1, 8, "", border_celdas_vacias_xfs)
    hoja_1.write_merge(2, 3, 8, 8, "", border_celdas_vacias_pagina_xfs)
    # fin
    fila = 4
    for row in range(1, len(resultado) + 1):
        for col in range(0, 9):
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
    hoja.merge_range('C1:I4', "PRODUCTOS EXISTENTES", titulo)
    hoja.write(0, 9, "Código:", estilo_cuerpo)
    hoja.write(1, 9, "Revisión:", estilo_cuerpo)
    hoja.merge_range('J3:J4', "Página:", estilo_cuerpo)
    hoja.write(0, 10, "", estilo_cuerpo)
    hoja.write(1, 10, "", estilo_cuerpo)
    hoja.merge_range('K3:K4', "", estilo_cuerpo)
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

# def exportar_compras_excel(request):
#     cursor = connection.cursor()
#     cursor.callproc("MOSTRAR_COMPRAS")
#     filas_datos = cursor.fetchall()
#     cont = 0
#     cont = [cont + 1 for row in filas_datos]

#     bordes = Border(left=Side(border_style=BORDER_THIN), top=Side(border_style=BORDER_THIN), right=Side(border_style=BORDER_THIN), bottom=Side(border_style=BORDER_THIN))
    
#     wb = Workbook()
#     ws = wb.active
#     ws.merge_cells('A1:B4')
#     fila_A1 = ws['A1']
#     fila_A1.border = bordes

#     filas_C1_G4 = ws['C1:G4']
#     for fila in filas_C1_G4:
#         fila[0].border = bordes

#     ws['C1'] = 'COMPRAS REALIZADAS'
#     ws.merge_cells('C1:G4')
#     fila_C1 = ws['C1']
#     fila_C1.font = Font(bold=True, color="00008000", size=20, name="Arial")
#     fila_C1.alignment = Alignment(horizontal="center", vertical="center")
#     fila_C1.border = bordes

#     fila_B1 = ws['A1']
#     fila_B1.font = Font(bold=True, color="00008000", size=20, name="Arial")
#     fila_B1.alignment = Alignment(horizontal="center", vertical="center")
#     ws['H1'] = 'Código:'
#     fila_H1 = ws['H1']
#     fila_H1.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_H1.alignment = Alignment(horizontal="left", vertical="center")
#     fila_H1.border = bordes
#     fila_I1 = ws['I1']
#     fila_I1.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_I1.alignment = Alignment(horizontal="left", vertical="center")
#     fila_I1.border = bordes
    
#     ws['H2'] = 'Revisión:'
#     fila_H2 = ws['H2']
#     fila_H2.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_H2.alignment = Alignment(horizontal="left", vertical="center")
#     fila_H2.border = bordes
#     fila_I2 = ws['I2']
#     fila_I2.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_I2.alignment = Alignment(horizontal="left", vertical="center")
#     fila_I2.border = bordes
    
#     filas_H3_H4 = ws['H3:H4']
#     for fila in filas_H3_H4:
#         fila[0].border = bordes
#     ws['H3'] = 'Página:'
#     ws.merge_cells('H3:H4')
#     fila_H3 = ws['H3']
#     fila_H3.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_H3.alignment = Alignment(horizontal="left", vertical="center")
#     fila_H3.border = bordes
#     filas_J3_J4 = ws['I3:J4']
#     for fila in filas_J3_J4:
#         fila[0].border = bordes
#     ws.merge_cells('I3:I4')
#     fila_H3 = ws['I3']
#     fila_H3.font = Font(bold=True, color="00000000", size=12, name="Arial")
#     fila_H3.alignment = Alignment(horizontal="left", vertical="center")
#     fila_H3.border = bordes

#     ws['A5'] = 'Id compra'
#     ws['A5'].font = Font(name="Arial", size=12)
#     ws['B5'] = 'Cod. detalle'
#     ws['B5'].font = Font(name="Arial", size=12)
#     ws['C5'] = 'Proveedor'
#     ws['C5'].font = Font(name="Arial", size=12)
#     ws['D5'] = 'Cod. producto'       
#     ws['D5'].font = Font(name="Arial", size=12)
#     ws['E5'] = 'Producto'
#     ws['E5'].font = Font(name="Arial", size=12)
#     ws['F5'] = 'Cantidad por producto'       
#     ws['F5'].font = Font(name="Arial", size=12)
#     ws['G5'] = 'Precio unitario'
#     ws['G5'].font = Font(name="Arial", size=12)
#     ws['H5'] = 'Medida'       
#     ws['H5'].font = Font(name="Arial", size=12)
#     ws['I5'] = 'Costo total'       
#     ws['I5'].font = Font(name="Arial", size=12)
#     filas = 6
    
#     for producto in cursor:
#         ws.cell(row=filas,column=1).value = producto[0]
#         ws.cell(row=filas,column=1).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=1).border = bordes
#         ws.cell(row=filas,column=2).value = producto[1]
#         ws.cell(row=filas,column=2).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=2).border = bordes
#         ws.cell(row=filas,column=3).value = producto[2]
#         ws.cell(row=filas,column=3).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=3).border = bordes
#         ws.cell(row=filas,column=4).value = producto[3]
#         ws.cell(row=filas,column=4).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=4).border = bordes
#         ws.cell(row=filas,column=5).value = producto[4]
#         ws.cell(row=filas,column=5).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=5).border = bordes
#         ws.cell(row=filas,column=6).value = producto[5]
#         ws.cell(row=filas,column=6).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=6).border = bordes
#         ws.cell(row=filas,column=7).value = producto[6]
#         ws.cell(row=filas,column=7).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=7).border = bordes
#         ws.cell(row=filas,column=8).value = producto[7]
#         ws.cell(row=filas,column=8).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=8).border = bordes
#         ws.cell(row=filas,column=9).value = producto[8]
#         ws.cell(row=filas,column=9).font = Font(name="Arial", size=11)
#         ws.cell(row=filas,column=9).border = bordes
#         if filas != cont * 2:
#             filas = filas + 1

#     nombre_archivo ="Compras.xlsx"
#     response = HttpResponse(content_type="application/ms-excel") 
#     contenido = "attachment; filename={0}".format(nombre_archivo)
#     response["Content-Disposition"] = contenido
#     wb.save(response)
#     cursor.close()
#     return response

def exportar_compras_xls(request):
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
    hoja_1.write_merge(0, 3, 2, 6, "COMPRAS REALIZADAS", titulo_xfs)
    hoja_1.write(0, 7, "Código:", estilo_encabezado)
    hoja_1.write(1, 7, "Revisión:", estilo_encabezado)
    hoja_1.write_merge(2, 3, 7, 7, "Página:", pagina_xfs)
    hoja_1.write(0, 8, "", border_celdas_vacias_xfs)
    hoja_1.write(1, 8, "", border_celdas_vacias_xfs)
    hoja_1.write_merge(2, 3, 8, 8, "", border_celdas_vacias_pagina_xfs)
    # fin

    # encabezado de tabla
    hoja_1.write(4, 0, "Compra", estilo_encabezado)
    hoja_1.write(4, 1, "Detalle", estilo_encabezado)
    hoja_1.write(4, 2, "Proveedor", estilo_encabezado)
    hoja_1.write(4, 3, "ID producto", estilo_encabezado)
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
    hoja.merge_range('C1:G4', "COMPRAS REALIZADAS", titulo)
    hoja.write(0, 7, "Código:", estilo_cuerpo)
    hoja.write(1, 7, "Revisión:", estilo_cuerpo)
    hoja.merge_range('H3:H4', "Página:", estilo_cuerpo)
    hoja.write(0, 8, "", estilo_cuerpo)
    hoja.write(1, 8, "", estilo_cuerpo)
    hoja.merge_range('I3:I4', "", estilo_cuerpo)
    # fin

    # campos del encabezado de la tabla
    hoja.write(4, 0, "Compra", estilo_cuerpo)
    hoja.write(4, 1, "Detalle", estilo_cuerpo)
    hoja.write(4, 2, "Proveedor", estilo_cuerpo)
    hoja.write(4, 3, "ID producto", estilo_cuerpo)
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

def exportar_ventas_excel(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.callproc("MOSTRAR_VENTAS")
        filas_datos = cursor.fetchall()
        cont = 0
        cont = [cont + 1 for row in filas_datos]
        
        bordes = Border(left=Side(border_style=BORDER_THIN), top=Side(border_style=BORDER_THIN), right=Side(border_style=BORDER_THIN), bottom=Side(border_style=BORDER_THIN))

        wb = Workbook()
        ws = wb.active
        ws.merge_cells('A1:B4')
        fila_A1 = ws['A1']
        fila_A1.border = bordes

        filas_C1_G4 = ws['C1:G4']
        for fila in filas_C1_G4:
            fila[0].border = bordes

        ws['C1'] = 'VENTAS REALIZADAS'
        ws.merge_cells('C1:G4')
        fila_C1 = ws['C1']
        fila_C1.font = Font(bold=True, color="00008000", size=20, name="Arial")
        fila_C1.alignment = Alignment(horizontal="center", vertical="center")
        fila_C1.border = bordes

        fila_B1 = ws['A1']
        fila_B1.font = Font(bold=True, color="00008000", size=20, name="Arial")
        fila_B1.alignment = Alignment(horizontal="center", vertical="center")
        ws['H1'] = 'Código:'
        fila_H1 = ws['H1']
        fila_H1.font = Font(bold=True, color="00000000", size=12, name="Arial")
        fila_H1.alignment = Alignment(horizontal="left", vertical="center")
        fila_H1.border = bordes
        fila_I1 = ws['I1']
        fila_I1.font = Font(bold=True, color="00000000", size=12, name="Arial")
        fila_I1.alignment = Alignment(horizontal="left", vertical="center")
        fila_I1.border = bordes
        
        ws['H2'] = 'Revisión:'
        fila_H2 = ws['H2']
        fila_H2.font = Font(bold=True, color="00000000", size=12, name="Arial")
        fila_H2.alignment = Alignment(horizontal="left", vertical="center")
        fila_H2.border = bordes
        fila_I2 = ws['I2']
        fila_I2.font = Font(bold=True, color="00000000", size=12, name="Arial")
        fila_I2.alignment = Alignment(horizontal="left", vertical="center")
        fila_I2.border = bordes
        
        filas_H3_H4 = ws['H3:H4']
        for fila in filas_H3_H4:
            fila[0].border = bordes
        ws['H3'] = 'Página:'
        ws.merge_cells('H3:H4')
        fila_H3 = ws['H3']
        fila_H3.font = Font(bold=True, color="00000000", size=12, name="Arial")
        fila_H3.alignment = Alignment(horizontal="left", vertical="center")
        fila_H3.border = bordes
        filas_J3_J4 = ws['I3:J4']
        for fila in filas_J3_J4:
            fila[0].border = bordes
        ws.merge_cells('I3:I4')
        fila_H3 = ws['I3']
        fila_H3.font = Font(bold=True, color="00000000", size=12, name="Arial")
        fila_H3.alignment = Alignment(horizontal="left", vertical="center")
        fila_H3.border = bordes

        ws['A5'] = 'Identificador'
        ws['A5'].font = Font(name="Arial", size=12)
        ws['B5'] = 'Producto'
        ws['B5'].font = Font(name="Arial", size=12)
        ws['C5'] = 'Descripción'
        ws['C5'].font = Font(name="Arial", size=12)
        ws['D5'] = 'Cantidad'       
        ws['D5'].font = Font(name="Arial", size=12)
        ws['E5'] = 'Medida'
        ws['E5'].font = Font(name="Arial", size=12)
        ws['F5'] = 'Departamento'       
        ws['F5'].font = Font(name="Arial", size=12)
        ws['G5'] = 'Precio unitario'
        ws['G5'].font = Font(name="Arial", size=12)
        ws['H5'] = 'Subtotal'       
        ws['H5'].font = Font(name="Arial", size=12)
        ws['I5'] = 'Precio total'       
        ws['I5'].font = Font(name="Arial", size=14)
        filas = 6
        
        for producto in cursor:
            ws.cell(row=filas,column=1).value = producto[0]
            ws.cell(row=filas,column=1).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=1).border = bordes
            ws.cell(row=filas,column=2).value = producto[1]
            ws.cell(row=filas,column=2).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=2).border = bordes
            ws.cell(row=filas,column=3).value = producto[2]
            ws.cell(row=filas,column=3).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=3).border = bordes
            ws.cell(row=filas,column=4).value = producto[3]
            ws.cell(row=filas,column=4).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=4).border = bordes
            ws.cell(row=filas,column=5).value = producto[4]
            ws.cell(row=filas,column=5).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=5).border = bordes
            ws.cell(row=filas,column=6).value = producto[5]
            ws.cell(row=filas,column=6).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=6).border = bordes
            ws.cell(row=filas,column=7).value = producto[6]
            ws.cell(row=filas,column=7).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=7).border = bordes
            ws.cell(row=filas,column=8).value = producto[7]
            ws.cell(row=filas,column=8).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=8).border = bordes
            ws.cell(row=filas,column=9).value = producto[8]
            ws.cell(row=filas,column=9).font = Font(name="Arial", size=11)
            ws.cell(row=filas,column=9).border = bordes
            if filas != cont * 2:
                filas = filas + 1

        nombre_archivo ="Ventas.xlsx"
        response = HttpResponse(content_type="application/ms-excel") 
        contenido = "attachment; filename={0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        cursor.close()
        return response
    else:
        return HttpResponse("<h1>No se pudo descargar el archivo<h1>")

# def exportar_diferentes_movimientos_excel(request):
#     if request.method == 'POST':
#         cursor = connection.cursor()
#         cursor.callproc("MOSTRAR_MOV_IND")
#         filas_datos = cursor.fetchall()
#         cont = 0
#         cont = [cont + 1 for row in filas_datos]
        
#         bordes = Border(left=Side(border_style=BORDER_THIN), top=Side(border_style=BORDER_THIN), right=Side(border_style=BORDER_THIN), bottom=Side(border_style=BORDER_THIN))

#         wb = Workbook()
#         ws = wb.active
#         ws.merge_cells('A1:B4')
#         fila_A1 = ws['A1']
#         fila_A1.border = bordes

#         filas_C1_G4 = ws['C1:G4']
#         for fila in filas_C1_G4:
#             fila[0].border = bordes

#         ws['C1'] = 'MOVIMIENTOS REALIZADOS'
#         ws.merge_cells('C1:G4')
#         fila_C1 = ws['C1']
#         fila_C1.font = Font(bold=True, color="00008000", size=20, name="Arial")
#         fila_C1.alignment = Alignment(horizontal="center", vertical="center")
#         fila_C1.border = bordes

#         fila_B1 = ws['A1']
#         fila_B1.font = Font(bold=True, color="00008000", size=20, name="Arial")
#         fila_B1.alignment = Alignment(horizontal="center", vertical="center")
#         ws['H1'] = 'Código:'
#         fila_H1 = ws['H1']
#         fila_H1.font = Font(bold=True, color="00000000", size=12, name="Arial")
#         fila_H1.alignment = Alignment(horizontal="left", vertical="center")
#         fila_H1.border = bordes
#         fila_I1 = ws['I1']
#         fila_I1.font = Font(bold=True, color="00000000", size=12, name="Arial")
#         fila_I1.alignment = Alignment(horizontal="left", vertical="center")
#         fila_I1.border = bordes
        
#         ws['H2'] = 'Revisión:'
#         fila_H2 = ws['H2']
#         fila_H2.font = Font(bold=True, color="00000000", size=12, name="Arial")
#         fila_H2.alignment = Alignment(horizontal="left", vertical="center")
#         fila_H2.border = bordes
#         fila_I2 = ws['I2']
#         fila_I2.font = Font(bold=True, color="00000000", size=12, name="Arial")
#         fila_I2.alignment = Alignment(horizontal="left", vertical="center")
#         fila_I2.border = bordes
        
#         filas_H3_H4 = ws['H3:H4']
#         for fila in filas_H3_H4:
#             fila[0].border = bordes
#         ws['H3'] = 'Página:'
#         ws.merge_cells('H3:H4')
#         fila_H3 = ws['H3']
#         fila_H3.font = Font(bold=True, color="00000000", size=12, name="Arial")
#         fila_H3.alignment = Alignment(horizontal="left", vertical="center")
#         fila_H3.border = bordes
#         filas_J3_J4 = ws['I3:J4']
#         for fila in filas_J3_J4:
#             fila[0].border = bordes
#         ws.merge_cells('I3:I4')
#         fila_H3 = ws['I3']
#         fila_H3.font = Font(bold=True, color="00000000", size=12, name="Arial")
#         fila_H3.alignment = Alignment(horizontal="left", vertical="center")
#         fila_H3.border = bordes

#         ws['A5'] = 'Id'
#         ws['A5'].font = Font(name="Arial", size=12)
#         ws['A5'].alignment = Alignment(horizontal="center", vertical="center")
#         ws['B5'] = 'Tipo de movimiento'
#         ws['B5'].font = Font(name="Arial", size=12)
#         ws['C5'] = 'Nombre de producto'
#         ws['C5'].font = Font(name="Arial", size=12)
#         ws['D5'] = 'Fecha'       
#         ws['D5'].font = Font(name="Arial", size=12)
#         ws['E5'] = 'Origen/Destino'
#         ws['E5'].font = Font(name="Arial", size=12)
#         ws['F5'] = 'Departamento'       
#         ws['F5'].font = Font(name="Arial", size=12)
#         ws['G5'] = 'Motivo'
#         ws['G5'].font = Font(name="Arial", size=12)
#         ws['H5'] = 'Cantidad'       
#         ws['H5'].font = Font(name="Arial", size=12)
#         ws['I5'] = 'Medida'       
#         ws['I5'].font = Font(name="Arial", size=14)
#         filas = 6
        
#         for producto in cursor:
#             ws.cell(row=filas,column=1).value = producto[0]
#             ws.cell(row=filas,column=1).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=1).border = bordes
#             ws.cell(row=filas,column=2).value = producto[1]
#             ws.cell(row=filas,column=2).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=2).border = bordes
#             ws.cell(row=filas,column=3).value = producto[2]
#             ws.cell(row=filas,column=3).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=3).border = bordes
#             ws.cell(row=filas,column=4).value = producto[3]
#             ws.cell(row=filas,column=4).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=4).border = bordes
#             ws.cell(row=filas,column=5).value = producto[4]
#             ws.cell(row=filas,column=5).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=5).border = bordes
#             ws.cell(row=filas,column=6).value = producto[5]
#             ws.cell(row=filas,column=6).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=6).border = bordes
#             ws.cell(row=filas,column=7).value = producto[6]
#             ws.cell(row=filas,column=7).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=7).border = bordes
#             ws.cell(row=filas,column=8).value = producto[7]
#             ws.cell(row=filas,column=8).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=8).border = bordes
#             ws.cell(row=filas,column=9).value = producto[8]
#             ws.cell(row=filas,column=9).font = Font(name="Arial", size=11)
#             ws.cell(row=filas,column=9).border = bordes
#             if filas != cont * 2:
#                 filas = filas + 1

#         nombre_archivo ="Otros_movimientos.xlsx"
#         response = HttpResponse(content_type="application/ms-excel") 
#         contenido = "attachment; filename={0}".format(nombre_archivo)
#         response["Content-Disposition"] = contenido
#         wb.save(response)
#         cursor.close()
#         return response
#     else:
#         return HttpResponse("<h1>No se pudo descargar el archivo<h1>")

def exportar_diferentes_movimientos_xls(request):
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
    hoja_1.write_merge(0, 3, 2, 4, "MOVIMIENTOS REALIZADOS", titulo_xfs)
    hoja_1.write(0, 5, "Código:", estilo_encabezado)
    hoja_1.write(1, 5, "Revisión:", estilo_encabezado)
    hoja_1.write_merge(2, 3, 5, 5, "Página:", pagina_xfs)
    hoja_1.write(0, 6, "", border_celdas_vacias_xfs)
    hoja_1.write(1, 6, "", border_celdas_vacias_xfs)
    hoja_1.write_merge(2, 3, 6, 6, "", border_celdas_vacias_pagina_xfs)
    # fin

    # encabezado de tabla
    hoja_1.write(4, 0, "Movimiento", estilo_encabezado)
    hoja_1.write(4, 1, "Tipo de movimiento", estilo_encabezado)
    hoja_1.write(4, 2, "Producto", estilo_encabezado)
    hoja_1.write(4, 3, "Fecha", estilo_encabezado)
    hoja_1.write(4, 4, "Origen o destino", estilo_encabezado)
    hoja_1.write(4, 5, "Departamento", estilo_encabezado)
    hoja_1.write(4, 6, "Motivo", estilo_encabezado)
    # fin

    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 7):
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
    hoja.merge_range('C1:E4', "MOVIMIENTOS REALIZADOS", titulo)
    hoja.write(0, 5, "Código:", estilo_cuerpo)
    hoja.write(1, 5, "Revisión:", estilo_cuerpo)
    hoja.merge_range('F3:F4', "Página:", estilo_cuerpo)
    hoja.write(0, 6, "", estilo_cuerpo)
    hoja.write(1, 6, "", estilo_cuerpo)
    hoja.merge_range('G3:G4', "", estilo_cuerpo)
    # fin

    # campos del encabezado de la tabla
    hoja.write(4, 0, "Movimiento", estilo_cuerpo)
    hoja.write(4, 1, "Tipo de movimiento", estilo_cuerpo)
    hoja.write(4, 2, "Producto", estilo_cuerpo)
    hoja.write(4, 3, "Fecha", estilo_cuerpo)
    hoja.write(4, 4, "Origen o destino",estilo_cuerpo)
    hoja.write(4, 5, "Departamento", estilo_cuerpo)
    hoja.write(4, 6, "Motivo", estilo_cuerpo)
    # fin
    fila = 5
    for row in range(1, len(resultado) + 1):
        for col in range(0, 7):
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
