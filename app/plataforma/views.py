from django.http import JsonResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.db import connections
from django.db import DatabaseError, IntegrityError, NotSupportedError, InterfaceError, OperationalError, ProgrammingError, InternalError
# Create your views here.
def index(request):
    context = {
        "title": "Mantenimiento preventivo",
        'email': request.session.get("email"),
        'privilegio': request.session.get("privilegio"),
    }
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.execute("SELECT * FROM maquinas_equipos")
        context["items"] = cursor.fetchall()
        cursor2 = connections["mcgreen_conexion"].cursor()
        cursor2.execute("SELECT * FROM frecuencia")
        context["frequence"] = cursor2.fetchall()
        cursor3 = connections["mcgreen_conexion"].cursor()
        cursor3.execute("SELECT * FROM actividades")
        context["activities"] = cursor3.fetchall()
    except (OperationalError, DatabaseError, InternalError) as e:
        print(e)
    return render(request, "Plataforma/index.html", context)

def activities(request):
    context = {
        "title": "Actividades",
        'email': request.session.get("email"),
        'privilegio': request.session.get("privilegio"),
    }
    return render(request, "Plataforma/activities.html", context)

def items(request):
    context = {
        "title": "Equipos",
        'email': request.session.get("email"),
        'privilegio': request.session.get("privilegio"),
    }
    return render(request, "Plataforma/items.html", context)

def item_view(request, id_item):
    context = {
        "item": id_item,
        'email': request.session.get("email"),
        'privilegio': request.session.get("privilegio"),
    }
    print("ID:",id_item)
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.callproc("CARACTERISTICAS_ITEM", [id_item])
        get_info = cursor.fetchall()
        ar = []
        for car in get_info:
            if car[1] == id_item:
                ar.append(car)
        context["caracteristicas"] = ar
        context["title"] = 'Item ' + id_item
    except (OperationalError, DatabaseError, ProgrammingError) as e:
        print(e)
    finally:
        cursor.close()
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.execute("SELECT * FROM estado_plat")
        get_info = cursor.fetchall()
        context["states"] = get_info
    except (OperationalError, DatabaseError, ProgrammingError) as e:
        print(e)
    finally:
        cursor.close()
    try:
        cursor2 = connections["mcgreen_conexion"].cursor()
        cursor2.callproc("MOSTRAR_PROVEEDOR_EN_ITEM", [id_item])
        get_pro = cursor2.fetchall()
        context["existe_prov"] = True if get_pro else False
        context["provider"] = get_pro
    except (OperationalError, DatabaseError, ProgrammingError) as e:
        print(e)
    finally:
        cursor2.close()
    try:
        cursor = connections["mcgreen_conexion"].cursor()
        cursor.execute("SELECT * FROM proveedores")
        get_pro = cursor.fetchall()
        context["providers"] = get_pro
    except (OperationalError, DatabaseError, ProgrammingError) as e:
        print(e)
    finally:
        cursor.close()
    try:
        return render(request, "Plataforma/item.html", context)
    except (TemplateDoesNotExist, TemplateSyntaxError) as er:
        print("Error en template:",er)
        return render(request, "errors/error500.html")

def correc_manteinment(request):
    context = {
        "title": "Mantenimiento correctivo",
        'email': request.session.get("email"),
        'privilegio': request.session.get("privilegio"),
    }
    return render(request, "Plataforma/manteinment.html", context)

def other_views(request):
    try:
        context = {
            "title": "Otros movimientos",
            'email': request.session.get("email"),
            'privilegio': request.session.get("privilegio"),
        }
        return render(request, "Plataforma/other.html", context)
    except (TemplateDoesNotExist, TemplateSyntaxError) as er:
        print("Error en template:",er)
        return render(request, "errors/error500.html")