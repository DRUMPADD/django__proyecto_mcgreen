from django.urls import path
from . import views
from .admin_vistas import vistas
from .posts import posts
from .RR_HH import vistas as vistas_rh
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion', views.cerrar_sesion, name="cerrar_sesion"),
    path('Inicio', views.inicio, name="inicio"),
    path('Registro', views.registro, name="registro"),
    path('registra_usuario', posts.registra_usuario, name="registra_usuario"),
    path('Inventario_general', views.Inventario_general, name="Inventario_general"),
    path('modificar_producto', posts.modificar_producto, name="modificar_producto"),
    path('descontinuar_producto/<str:id_prod>', posts.descontinuar_producto, name="descontinuar_producto"),
    path('activar_producto/<str:id_prod>', posts.activar_producto, name="activar_producto"),
    path('Compras', views.compras, name="compras"),
    path('Ventas', views.ventas, name="ventas"),
    path('Otras_E_S', views.otras_e_s, name="otras_e_s"),
    path('agregar_otros', posts.agregar_otros, name="agregar_otros"),
    path('Movimientos', views.movimientos, name="movimientos"),
    path('Ver_compras', views.ver_compras, name="ver_compras"),
    path('Ver_cuentas_por_cobrar', views.ver_cuentas_p_c, name="Ver_cuentas_por_cobrar"),
    path('Ver_ventas', views.ver_ventas, name="ver_ventas"),
    path('Ver_otras', views.ver_otros, name="ver_otros"),
    path('generar_compra', posts.generar_compra, name="generar_compra"),
    path('generar_venta', posts.generar_venta, name="generar_venta"),
    path('cuenta_por_cobrar', posts.generar_cuenta_por_cobrar, name="cuenta_por_cobrar"),
    path('modificar_cuenta', posts.modificar_cuenta_por_cobrar, name="modificar_cuenta"),
    path('inventario/agrega_producto', posts.agregar_producto, name="agregar_producto"),
    path('proveedores/agregar_proveedores', posts.agregar_proveedores, name="agregar_proveedores"),
    path('clientes/agregar_clientes', posts.agregar_clientes, name="agregar_clientes"),
    path('Usuarios', vistas.usuarios, name="usuarios"),
    path('Auditoria', vistas.auditoria, name="Auditoria"),
    path('descargar_inv_xls/', posts.exportar_inventario_xls, name="descargar_inv_xls"),
    path('descargar_inv_xlsx/', posts.exportar_inventario_xlsx, name="descargar_inv_xlsx"),
    path('convertir_com_xls/', posts.exportar_compras_xls, name="convertir_com_xls"),
    path('convertir_com_xlsx/', posts.exportar_compras_xlsx, name="convertir_com_xlsx"),
    path('convertir_vta_xls/', posts.exportar_ventas_xls, name="convertir_vta_xls"),
    path('convertir_vta_xlsx/', posts.exportar_ventas_xlsx, name="convertir_vta_xlsx"),
    path('convertir_difmov_xls/', posts.exportar_diferentes_movimientos_xls, name="convertir_difmov_xls"),
    path('convertir_difmov_xlsx/', posts.exportar_diferentes_movimientos_xlsx, name="convertir_difmov_xlsx"),
    # ?? Recursos humanos
    path("Directorio", vistas_rh.directorio, name="directorio"),
    path("Perfil_puesto", vistas_rh.perfil_puesto, name="perfil_puesto"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)