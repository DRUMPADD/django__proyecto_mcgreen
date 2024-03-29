from django.shortcuts import redirect, render
from . import models
from django.db import IntegrityError, InternalError, OperationalError, connection
from .forms import formulario_cliente, formulario_proveedor, Formulario_registro

# Create your views here.
# ?? Sesiones
def iniciar_sesion(request):
    if request.session.get("email"):
        return redirect("/Inicio")
    else:
        if request.method == 'POST':
            try:
                cursor = connection.cursor()
                departamento = connection.cursor()
                cursor.execute("Select privilegio_id from app_usuarios where email = %s",[request.POST["user"]])
                privilegio = cursor.fetchone()
                departamento.execute("select id_dep_id from app_usuarios ap_u, app_empleados ap_e, app_puestos ap_p, app_departamento ap_d where ap_u.empleado_id = ap_e.id_empleado and ap_e.puesto_id = ap_p.id_puesto and ap_p.id_dep_id = ap_d.id_dep and ap_u.email = %s",[request.POST["user"]])
                departamento_selec = departamento.fetchone() 
                cursor.callproc("VERIFICAR_USUARIO",[request.POST["user"], request.POST["pass"]])
                mensaje = cursor.fetchone()[0]
                if mensaje == 'EXISTE':
                    request.session["email"] = request.POST["user"]
                    request.session["departamento"] = departamento_selec[0]
                    request.session["privilegio"] = privilegio[0]
                    request.session.modified = True
                    cursor.close()
                    return redirect("/Inicio")
                else:
                    cursor.close()
                    return redirect("usuario_no_encontrado")
            except (OperationalError, IntegrityError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
        return render(request, 'login.html')

def inicio(request):
    if request.session.get("email"):
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_USUARIOS")
            usuarios = cursor.fetchall()
        except (InternalError, OperationalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()

        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_MIS_ACTIVIDADES", [request.session.get("email")])
            actividades = cursor.fetchall()
        except (InternalError, OperationalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()

        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_MIS_EVENTOS_HOY", [request.session.get("email")])
            eventos = cursor.fetchall()
        except (InternalError, OperationalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        context = {
            'privilegio': request.session.get("privilegio"),
            'usuarios': usuarios,
            'eventos': eventos,
            'actividades': actividades,
        }
        return render(request, "inicio.html", context)
    else:
        return redirect("/cerrar_sesion")

def registro(request):
    if request.session.get('email'):
        formulario = Formulario_registro()
        return render(request, 'registro.html', {'formulario': formulario, 'privilegio': request.session.get("privilegio")})
    else:
        return redirect("/cerrar_sesion")


def cerrar_sesion(request):
    try:
        cursor = connection.cursor()
        cursor.callproc("AUDITORIA", [request.session.get('email'), "cerró sesión"])
        cursor.close()
        del request.session["email"]
        del request.session["departamento"]
        del request.session["privilegio"]
    except (KeyError, IntegrityError, OperationalError) as e:
        print(e)
        return render(request, "errors/error500.html", {
            "mensaje": "Contacte con el servicio de sistemas"
        })
    return render(request, "Inventario/cerrar_sesion.html")

# ?? Inventario
def Inventario_general(request):
    if request.session.get("email"):
        if request.session.get("privilegio") != 'ADM-IN1' and request.session.get("privilegio") != 'JEFE':
            try:
                cursor = connection.cursor()
                cursor.callproc('MOSTRAR_PRODUCTOS_ACTIVOS')
                nombres = [
                    models.Inventario._meta.get_field("id_producto").name,
                    models.Inventario._meta.get_field("nombre_producto").name,
                    models.Inventario._meta.get_field("descripcion").name,
                    models.Inventario._meta.get_field("cantidad").name,
                    models.Inventario._meta.get_field("medida").name,
                    models.Inventario._meta.get_field("id_dep_id").name,
                    "Precio unitario",
                    "IVA",
                    "Precio total",
                    "Tipo de cambio",
                    "Sucursal"
                ]
                context = {
                    'departamentos': models.Departamento.objects.all(),
                    'inventario': cursor.fetchall(),
                    'campos_inv': nombres,
                    'privilegio': request.session.get("privilegio"),
                }
            except (OperationalError, IntegrityError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
            return render(request, 'Inventario/index.html', context)
        else:
            try:
                cursor = connection.cursor()
                cursor.callproc('MOSTRAR_TODOS_LOS_PRODUCTOS')
                nombres = [
                    models.Inventario._meta.get_field("id_producto").name,
                    models.Inventario._meta.get_field("nombre_producto").name,
                    models.Inventario._meta.get_field("descripcion").name,
                    models.Inventario._meta.get_field("cantidad").name,
                    models.Inventario._meta.get_field("medida").name,
                    models.Inventario._meta.get_field("id_dep_id").name,
                    "Precio unitario",
                    "Subtotal",
                    "Precio total",
                    "Estado",
                    "Tipo de cambio",
                    "Sucursal",
                ]
                context = {
                    'departamentos': models.Departamento.objects.all(),
                    'inventario': cursor.fetchall(),
                    'campos_inv': nombres,
                    'privilegio': request.session.get("privilegio"),
                    'departamento': request.session.get("departamento"),
                }
            except (OperationalError, IntegrityError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
            return render(request, 'Inventario/index.html', context)
    else:
        return redirect("/cerrar_sesion")

# ?? Compras
def compras(request):
    if request.session.get('email'):
        if request.method != 'POST':
            try:
                proveedores = connection.cursor()
                cursor = connection.cursor()
                proveedores.execute("select * from app_proveedor where sector = 'VARIOS'")
                cursor.callproc('MOSTRAR_PRODUCTOS_ACTIVOS')
                form = formulario_proveedor()

                context = {
                    'productos': cursor.fetchall(),
                    'proveedores': proveedores.fetchall(),
                    'form': form,
                    'sesion': request.session.get("email"),
                    'privilegio': request.session.get("privilegio")
                }
            except (OperationalError, IntegrityError) as e:
                print(e)
                return render(request, "errors/error500.html", {
                    "mensaje": "Contacte con el servicio de sistemas"
                })
            finally:
                cursor.close()
                proveedores.close()
            return render(request, 'Inventario/compras.html', context)
    else:
        return redirect("/cerrar_sesion")



# ?? Ventas
def ventas(request):
    if request.session.get('email'):
        if request.method != 'POST':
            try:
                clientes = connection.cursor()
                cursor = connection.cursor()
                cursor.callproc('MOSTRAR_SISTEMAS_ACTIVOS')
                form = formulario_cliente()
                clientes.execute("SELECT * FROM app_clientes where sector = 'VARIOS' ")
                res_clientes = clientes.fetchall()
                context = {
                    'sistemas': cursor.fetchall(),
                    'clientes': res_clientes,
                    'sesion': request.session.get("email"),
                    'privilegio': request.session.get("privilegio"),
                    'form': form,
                }
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
                clientes.close()
            return render(request, 'Inventario/cuentas_p_c.html', context)
    else:
        return redirect("/cerrar_sesion")

# ?? Otros tipos de movimientos
def otras_e_s(request):
    if request.session.get('email'):
        try:
            cursor = connection.cursor()
            cursor.callproc('MOSTRAR_TODOS_LOS_PRODUCTOS')
            context = {
                'sesion': request.session.get("email"),
                'privilegio': request.session.get("privilegio"),
                'productos': cursor.fetchall(),
            }
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        return render(request, 'Inventario/otras_e_s.html', context)
    else:
        return redirect("/cerrar_sesion")


def movimientos(request):
    if request.session.get('email'):
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_MOV_IND")
            context = {
                'movimientos': cursor.fetchall()
            }
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        context["privilegio"] = request.session.get("privilegio")
        return render(request, 'Inventario/movimientos.html', context)
    else:
        return redirect("/cerrar_sesion")


# ?? Vistas
def ver_compras(request):
    if request.session.get('email'):
        try:
            cursor = connection.cursor()
            cursor.callproc('MOSTRAR_COMPRAS')
            context = {
                'datos_compras': cursor.fetchall()
            }
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        return render(request, 'Inventario/ver_compras.html', context)
    else:
        return redirect("/cerrar_sesion")

def ver_ventas(request):
    if request.session.get('email'):
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_MOV_IND")
            context = {
                'movimientos': cursor.fetchall()
            }
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        return render(request, 'Inventario/ver_ventas.html', context)
    else:
        return redirect("/cerrar_sesion")

def ver_cuentas_p_c(request):
    if request.session.get('email'):
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_VENTAS_MOD")
            context = {
                'movimientos': cursor.fetchall(),
                'email': request.session.get('email')
            }
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        return render(request, 'Inventario/ver_cuentas_pc.html', context)
    else:
        return redirect("/cerrar_sesion")

def ver_otros(request):
    if request.session.get('email'):
        try:
            cursor = connection.cursor()
            cursor.callproc("MOSTRAR_MOV_IND")
            context = {
                'movimientos': cursor.fetchall()
            }
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        return render(request, 'Inventario/ver_otros.html', context)
    else:
        return redirect("/cerrar_sesion")

def vista_quimico(request):
    if request.session.get("email"):
        context = {
            'titulo': 'Quimico',
            'email': request.session.get("email"),
            "privilegio": request.session.get("privilegio"),
        }
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * from app_inventario")
            context["productos"] = cursor.fetchall()
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * from app_inventario where nombre_producto like '%sistema%'")
            context["sistemas"] = cursor.fetchall()
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * from app_departamento")
            context["departamentos"] = cursor.fetchall()
        except (OperationalError, IntegrityError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        
        return render(request, "Inventario/sistema.html", context)
    else:
        return redirect("/cerrar_sesion")

def error_usuario_no_existe(request):
    return render(request, 'errors/usuario_no_existe.html')