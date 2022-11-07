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
from .accidentabilidad import views as v_acc
from .accidentabilidad import posts as p_acc
from .plataforma import views as v_plat
from .plataforma.requests import re as v_plat
from .plataforma.requests import activity_requests as plat_act_req
from .plataforma.requests import items_requests as plat_it_req
from .plataforma.requests import general_requests as plat_g_req
from .plataforma.requests import manteinment_requests as plat_mnt_req
from .plataforma.requests import providers_requests as plat_pro_req
from .plataforma.requests import frequences_requests as plat_fec_req
from .plataforma.requests import novelties_requests as plat_nov_req
from .plataforma.requests import modes_requests as plat_mod_req
from .plataforma.requests import state_mant_requests as plat_st_req

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
    path('subir_evidencia', p_sigss.subir_evidencia_despues, name="subir_evidencia"),
    path('cliente_sigssmac', p_sigss.agregar_cliente_sigssmac, name="cliente_sigssmac"),
    # ?? Accidentabilidad
    path("vista_accidentabilidad", v_acc.accidentabilidad_vista, name="acci_vista"),
    path("datos_generales_obtenidos", v_acc.datos_x_meses, name="datos_generales_obtenidos"),
    path("registrar_acci", p_acc.accidentabilidad_post, name="registrar_info"),


    # ?? Plataforma industrial
    path("mantenimiento-general", v_plat.index, name="generalMant"),
    path("actividades", v_plat.activities, name="activities"),
    path("equipos", v_plat.items, name="items"),
    path("mantenimiento-correctivo", v_plat.correc_manteinment, name="corMant"),
    path("otros-registros", v_plat.other_views, name="otherRegisters"),
    # ? General manteinment requests
    path("plataforma/general/mostrarGeneral", plat_g_req.show_general_mant, name="showGeneralMnt"),
    path("plataforma/general/crearGeneral", plat_g_req.create_general, name="createGeneralMnt"),
    path("plataforma/general/modificarGeneral", plat_g_req.modify_general, name="modifyGeneralMnt"),
    path("plataforma/general/eliminarGeneral", plat_g_req.delete_general, name="deleteGeneralMnt"),
    # ? Activities requests
    path("plataforma/actividades/crear_actividad", plat_act_req.create_activity, name="createActivity"),
    path("plataforma/actividades/modificarActividad", plat_act_req.modify_activity, name="modifyActivity"),
    path("plataforma/actividades/mostrarActividad", plat_act_req.show_activities, name="showAcivities"),
    path("plataforma/actividades/buscarActividad", plat_act_req.search_activity, name="searchActivity"),
    path("plataforma/actividades/eliminarActividad", plat_act_req.delete_activity, name="deleteActivity"),
    path("plataforma/actividades/eliminarActividadCompleto", plat_act_req.delete_activity_with_mant, name="deleteAllActivity"),
    # ? Items requests
    path("plataforma/equipo/mostrarItems", plat_it_req.show_items, name="showItems"),
    path("plataforma/equipo/modificarItem", plat_it_req.modify_item, name="modifyItems"),
    path("plataforma/equipo/info_item/<slug:id_item>", v_plat.item_view, name="item"),
    path("plataforma/equipo/registrarItem", plat_it_req.create_item, name="createItem"),
    path("plataforma/equipo/buscarItem", plat_it_req.search_item, name="searchItem"),
    path("plataforma/equipo/eliminarItem", plat_it_req.delete_item, name="deleteItem"),
    path("plataforma/equipo/eliminarItemCompleto", plat_it_req.delete_item_complete, name="deleteCompleteItem"),
    path("plataforma/equipo/modificarCaracteristicas", plat_it_req.modify_carateristics, name="modifyCaracteristics"),
    # ? Manteinment requests
    path("plataforma/correctivo/mostrarCorrectivo", plat_mnt_req.show_corrective_mant, name="showManteinments"),
    path("plataforma/correctivo/agregarCorrectivo", plat_mnt_req.create_manteinment, name="createManteinment"),
    path("plataforma/correctivo/modificarCorrectivo", plat_mnt_req.modify_manteinment, name="modifyManteinment"),
    path("plataforma/correctivo/eliminarCorrectivo", plat_mnt_req.delete_manteinment, name="deleteManteinment"),
    # ? Provider requests
    path("plataforma/proveedor/mostrarProveedores", plat_pro_req.show_providers, name="showProviders"),
    path("plataforma/proveedor/agregarProveedor", plat_pro_req.create_provider, name="createProviders"),
    path("plataforma/proveedor/agregarProveedorAItem", plat_pro_req.add_provider_to_item, name="addProviderToItem"),
    path("plataforma/proveedor/modificarProveedor", plat_pro_req.modify_provider, name="modifyProviders"),
    path("plataforma/proveedor/eliminarProveedor", plat_pro_req.delete_provider, name="deleteProviders"),
    path("plataforma/proveedor/cambiarProveedor", plat_pro_req.change_provider, name="changeProviderToItem"),
    path("plataforma/proveedor/buscarProveedor", plat_pro_req.search_provider, name="searchProvider"),
    path("plataforma/proveedor/quitarProveedor", plat_pro_req.delete_provider_from_item, name="removeProviderToItem"),
    # ? Other requests
    path("plataforma/estado/mostrarEstados", plat_st_req.showStates, name="showStates"),
    path("plataforma/estado/crearEstado", plat_st_req.createState, name="createState"),
    path("plataforma/estado/modificarEstado", plat_st_req.modifyState, name="modifyState"),
    path("plataforma/estado/eliminarEstado", plat_st_req.deleteState, name="deleteState"),
    path("plataforma/estado/buscarEstado", plat_st_req.searchState, name="searchState"),
    path("plataforma/frecuencia/mostrarFrecuencias", plat_fec_req.showFrequences, name="showFrequences"),
    path("plataforma/frecuencia/crearFrecuencia", plat_fec_req.createFrequence, name="createFrequence"),
    path("plataforma/frecuencia/modificarFrecuencia", plat_fec_req.modifyFrequence, name="modifyFrequence"),
    path("plataforma/frecuencia/eliminarFrecuencia", plat_fec_req.deleteFrequence, name="deleteFrequence"),
    path("plataforma/frecuencia/buscarFrecuencia", plat_fec_req.searchFrequence, name="searchFrequence"),
    path("plataforma/novedad/mostrarNovedades", plat_nov_req.showNovelties, name="showNovelties"),
    path("plataforma/novedad/crearNovedad", plat_nov_req.createNovelty, name="createNovelty"),
    path("plataforma/novedad/modificarNovedad", plat_nov_req.modifyNovelty, name="modifyNovelty"),
    path("plataforma/novedad/eliminarNovedad", plat_nov_req.deleteNovelty, name="deleteNovelty"),
    path("plataforma/novedad/buscarNovedad", plat_nov_req.searchNovelty, name="searchNovelty"),
    path("plataforma/modoFallo/mostrarModos", plat_mod_req.showModes, name="showModes"),
    path("plataforma/modoFallo/crearModo", plat_mod_req.createMode, name="createMode"),
    path("plataforma/modoFallo/modificarModo", plat_mod_req.modifyMode, name="modifyMode"),
    path("plataforma/modoFallo/eliminarModo", plat_mod_req.deleteMode, name="deleteMode"),
    path("plataforma/modoFallo/buscarModo", plat_mod_req.searchMode, name="searchMode"),
]