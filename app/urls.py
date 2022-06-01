from django.urls import path
from . import views
from .admin_vistas import vistas
from .posts import posts
from .RR_HH import vistas as vistas_rh
from .RR_HH import posts as posts_rh
from .indicadores import views as v_indic
from .indicadores import posts as p_indic
from .mantenimiento import views as mant
from .mantenimiento import posts as mant_post
from .sigssmac import vistas as v_sigss
from .sigssmac import posts as p_sigss

urlpatterns = [
    path('', views.iniciar_sesion, name="iniciar_sesion"),
    path('usuario_no_encontrado', views.error_usuario_no_existe, name="usuario_no_encontrado"),
    path('cerrar_sesion', views.cerrar_sesion, name="cerrar_sesion"),
    path('Inicio', views.inicio, name="inicio"),
    path('Registro', views.registro, name="registro"),
    path('registra_usuario', posts.registra_usuario, name="registra_usuario"),
    path('Inventario_general', views.Inventario_general, name="Inventario_general"),
    path('modificar_producto', posts.modificar_producto, name="modificar_producto"),
    path('modificar_producto_admin', posts.modificar_producto_cantidad, name="modificar_producto_admin"),
    path('descontinuar_producto/<str:id_prod>', posts.descontinuar_producto, name="descontinuar_producto"),
    path('activar_producto/<str:id_prod>', posts.activar_producto, name="activar_producto"),
    path('Compras', views.compras, name="compras"),
    path('Ventas', views.ventas, name="ventas"),
    path('Otras_E_S', views.otras_e_s, name="otras_e_s"),
    path('agregar_otros', posts.agregar_otros, name="agregar_otros"),
    path('Movimientos', views.movimientos, name="movimientos"),
    path('Ver_compras', views.ver_compras, name="ver_compras"),
    path("crear_sistema", views.vista_quimico, name="crear_sistema"),
    path("registrar_sistema", posts.registrar_sistema, name="registrar_sistema"),
    path('Ver_cuentas_por_cobrar', views.ver_cuentas_p_c, name="Ver_cuentas_por_cobrar"),
    path('Ver_ventas', views.ver_ventas, name="ver_ventas"),
    path('Ver_otras', views.ver_otros, name="ver_otros"),
    path('generar_compra', posts.generar_compra, name="generar_compra"),
    path('generar_venta', posts.generar_venta, name="generar_venta"),
    path('cuenta_por_cobrar', posts.generar_cuenta_por_cobrar, name="cuenta_por_cobrar"),
    path('modificar_cuenta', posts.modificar_cuenta_por_cobrar, name="modificar_cuenta"),
    path('crear_evento', posts.crear_evento, name="crear_evento"),
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
    path("perfil_y_directorio", vistas_rh.directorio_perfil, name="perfil_y_directorio"),
    path("crear_perfil_puesto", posts_rh.crear_perfil, name="creacion_perfil_puesto"),
    path("crear_directorio", posts_rh.crear_directorio, name="crear_directorio"),
    path("actualizar_perfil", posts_rh.actualizar_perfil, name="actualizar_perfil"),
    path("rrhh_detalles", vistas_rh.rrhh_detalles, name="rrhh_detalles"),
    path("funcion1", posts_rh.funcion1, name="funcion1"),
    path("funcion2", posts_rh.funcion2, name="funcion2"),
    path("funcion3", posts_rh.funcion3, name="funcion3"),
    path("funcion4", posts_rh.funcion4, name="funcion4"),
    path("funcion5", posts_rh.funcion5, name="funcion5"),
    path("funcion6", posts_rh.funcion6, name="funcion6"),
    path("funcion7", posts_rh.funcion7, name="funcion7"),
    path("funcion8", posts_rh.funcion8, name="funcion8"),
    path("funcion9", posts_rh.funcion9, name="funcion9"),
    path("actualizar_gen", posts_rh.actualizar_gen, name="actualizar_gen"),
    path("eliminar_subordinado", posts_rh.eliminar_subordinado, name="eliminar_subordinado"),
    path("eliminar_supervisor", posts_rh.eliminar_supervisor, name="eliminar_supervisor"),
    path("eliminar_funcion", posts_rh.eliminar_funcion, name="eliminar_funcion"),
    path("eliminar_res_ad", posts_rh.eliminar_res_ad, name="eliminar_res_ad"),
    path("eliminar_com_gen", posts_rh.eliminar_com_gen, name="eliminar_com_gen"),
    path("eliminar_com_tec", posts_rh.eliminar_com_tec, name="eliminar_com_tec"),
    path("eliminar_asp_ssmac", posts_rh.eliminar_asp_ssmac, name="eliminar_asp_ssmac"),
    path("eliminar_requer_fis", posts_rh.eliminar_requer_fis, name="eliminar_requer_fis"),
    path("ver_perfil/<str:nombre_perfil>", vistas_rh.mostrar_perfil_url, name="ver_perfil"),
    path("ver_personal/<str:id_empleado>", vistas_rh.vista_directorio, name="ver_personal"),
    path("eventos", vistas_rh.vista_eventos, name="eventos_tareas"),
    path("actualizar_tarea", posts_rh.actualizar_actividad, name="actualizar_tarea"),
    path("enviar_img", posts_rh.subir_imagen, name="enviar_img"),
    path("enviar_img", posts_rh.subir_imagen, name="enviar_img"),
    # ?? Indicadores
    path("indicadores", v_indic.vista_graficas, name="indicadores"),
    path("mostrar_grafica", p_indic.mostrar_grafica, name="mostrar_grafica"),
    # ?? Mantenimiento
    path("Mantenimiento", mant.vista_mantenimiento, name="mantenimiento"),
    path("crear_tarea", mant_post.crear_tarea, name="crear_tarea"),
    path("modificar_mant", mant_post.modificar_mant, name="modificar_mant"),
    # ?? Sigssmac
    path("sigssmac_vista", v_sigss.sigssmac_vista, name="sigssmac_vista"),
    path("sigssmac_post", p_sigss.sigssmac_post, name="sigssmac_post"),
]