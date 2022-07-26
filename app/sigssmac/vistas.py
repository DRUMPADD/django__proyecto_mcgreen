from django.shortcuts import redirect, render
from django.db import connection, IntegrityError, InternalError, OperationalError

def sigssmac_vista(request):
    if request.session.get("email"):
        context = {
            'email': request.session.get("email"),
            'privilegio': request.session.get("privilegio"),
        }
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM app_clientes where sector = 'P-SIGSSMAC'")
            context["clientes"] = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        texto = 'sigssmac.com'
        sigssmac_texto = f'%{texto}%'
        try:
            cursor = connection.cursor()
            cursor.execute("select email from app_usuarios where email like %s and email = '%s'" % (sigssmac_texto, request.session.get("email")))
            existe_ = cursor.fetchall()
            print(existe_)
            print(len(existe_))
            context["existe"] = 'SI EXISTE' if len(existe_) > 0 else 'NO EXISTE'
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM app_proveedor where sector = 'P-SIGSSMAC'")
            context["proveedores"] = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        try:
            cursor = connection.cursor()
            cursor.callproc("SIGSSMAC_REPORTES")
            context["detalles"] = cursor.fetchall()
        except (OperationalError, IntegrityError, InternalError) as e:
            print(e)
            return render(request, "errors/error500.html", {
                "mensaje": "Contacte con el servicio de sistemas"
            })
        finally:
            cursor.close()
        # try:
        #     cursor = connection.cursor()
        #     cursor.callproc("SIGSSMAC_REPORTES2")
        #     context["detalles2"] = cursor.fetchall()
        # except (OperationalError, IntegrityError, InternalError) as e:
        #     print(e)
        #     return render(request, "errors/error500.html", {
        #         "mensaje": "Contacte con el servicio de sistemas"
        #     })
        # finally:
        #     cursor.close()
        return render(request, "SIGSSMAC/sigssmac.html", context)
    else:
        return redirect("/cerrar_sesion")