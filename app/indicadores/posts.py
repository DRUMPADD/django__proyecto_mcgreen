from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db import IntegrityError, OperationalError, connection

def mostrar_grafica(request):
    datos = None
    if request.method == 'POST' and request.is_ajax():
        fecha_I = request.POST.get("fecha_inicio")
        fecha_T = request.POST.get("fecha_termino")
        c_seleccionada = request.POST.get("compra")
        v_seleccionada = request.POST.get("venta")
        o_seleccionado = request.POST.get("otro_mov")
        productos_seleccionados = request.POST.getlist("sl_productos")
        prod_exis = ['', '', '']
        for i in range(0, len(productos_seleccionados)):
            if productos_seleccionados[i] != None:
                prod_exis[i] = productos_seleccionados[i]
            else:
                prod_exis[i] = ""
        if c_seleccionada != None or v_seleccionada != None or o_seleccionado != None:
            fechas_ = []
            cantidades_c = []
            cantidades_v = []
            cantidades_i = []
            cantidades_co = []
            try:
                cursor = connection.cursor()
                cursor.callproc("ESTADISTICAS", [request.POST.get("opcion_vista"), fecha_I, fecha_T, "", "", ""])
                datos = cursor.fetchall()                
            except (OperationalError, IntegrityError):
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
            try: 
                est_general = connection.cursor()
                est_general.callproc("ESTADISTICAS_GRAFICA", [request.POST.get("opcion_vista"), "", fecha_I, fecha_T])
                estadisticas_obt = est_general.fetchall()
                for est_ in range(0, len(estadisticas_obt)):
                    if estadisticas_obt[est_][0] not in fechas_:
                        fechas_.append(estadisticas_obt[est_][0])
                    if estadisticas_obt[est_][2] == 'compra':
                        cantidades_c.append(estadisticas_obt[est_][1])
                    if estadisticas_obt[est_][2] == 'venta':
                        cantidades_v.append(estadisticas_obt[est_][1])
                    if estadisticas_obt[est_][2] == 'ingreso':
                        cantidades_i.append(estadisticas_obt[est_][1])
                    if estadisticas_obt[est_][2] == 'consumo':
                        cantidades_co.append(estadisticas_obt[est_][1])
            except (OperationalError, IntegrityError):
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                est_general.close()
            return JsonResponse({"datos": datos, "fechas": fechas_, "c_compras": cantidades_c, "c_ventas": cantidades_v, "c_ingresos": cantidades_i, "c_consumos": cantidades_co}, status=200)
        else:
            productos_dic = {}
            try:
                cursor = connection.cursor()
                cursor.callproc("ESTADISTICAS", [request.POST.get("opcion_vista"), fecha_I, fecha_T, prod_exis[0], prod_exis[1], prod_exis[2]])
                datos = cursor.fetchall()
            except (OperationalError, IntegrityError):
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
            try:
                for producto_ in (prod_exis):
                    if producto_ != '':
                        est_producto = connection.cursor()
                        est_producto.callproc("ESTADISTICAS_GRAFICA", [request.POST.get("opcion_vista"), producto_, fecha_I, fecha_T])
                        productos_dic[producto_] = est_producto.fetchall()
                        est_producto.close()
            except (OperationalError, IntegrityError):
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            return JsonResponse({"datos": datos, "productos": productos_dic}, status=200)
    else:
        return redirect("indicadores")