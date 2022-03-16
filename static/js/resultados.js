$(document).ready(function () {
    const ctx = document.getElementById('canvas_general').getContext('2d');
    $("#contenedor_canvas").hide();
    function limpiar_todo() {
        $("#tabla_general").hide();
        $("#tabla_productos").hide();
        $("#t_detalles_prod").hide();
        $("#contenedor_canvas").hide();
        $("#contenedor_canvas_prod").hide();
        $("#response").empty();
        $("#response2").empty();
        $(".t_detalles_body").empty();
        $("form").trigger("reset");
        $("#h1_info").hide();
        $("#h2_detalle").hide();
        if($(".otro_producto_copia")) {
            $(".otro_producto_copia").remove();
        }
        if(contador > 1) {
            contador = 1;
            $("#contador").text(contador);
        }
        if(myChart) {
            myChart.destroy();
        }
        
        if(charts) {
            charts.destroy();
        }
    }
    let myChart;
    function generar_grafica(fechas, compras, ventas, ingresos, consumos) {
        if(compras === undefined){ 
            compras = {
                label: 'Compras',
                data: [0]
            }
        }
        if(ventas === undefined){ 
            ventas = {
                label: 'Ventas',
                data: [0]
            }
        }
        if(ingresos === undefined){ 
            ingresos = {
                label: 'Ingresos',
                data: [0]
            }
        }
        if(consumos === undefined){ 
            consumos = {
                label: 'Consumos',
                data: [0]
            }
        }
        
        $("#contenedor_canvas").show();
        if(myChart) {
            myChart.destroy();
        }
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: fechas,
                datasets: [
                    compras,
                    ventas,
                    ingresos,
                    consumos
                ]
            },
            plugins: [ChartDataLabels],
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                },
                distribution: 'linear',
                responsive: true,
                legend: {
                    display: true,
                    labels: {
                        fontColor: 'rgb(255, 99, 132)',
                        fontFamily: "'Arial', 'sans-serif'",
                        fontSize: 20
                    },
                },
                plugins: {
                    datalabels: {
                        labels: {
                            title: {
                                font: {
                                    weight: 'bold',
                                    size: 16
                                }
                            },
                        },
                        anchor: 'end',
                        align: 'top'
                    }
                }
            }
        })
    }

    var charts;
    function graficas_producto(num, fechas, compras, ventas, ingresos, consumos) {
        if(compras === undefined){ 
            compras = {
                label: 'Compras',
                data: [0]
            }
        }
        if(ventas === undefined){ 
            ventas = {
                label: 'Ventas',
                data: [0]
            }
        }
        if(ingresos === undefined){ 
            ingresos = {
                label: 'Ingresos',
                data: [0]
            }
        }
        if(consumos === undefined){ 
            consumos = {
                label: 'Consumos',
                data: [0]
            }
        }
        if(charts) {
            charts.destroy();
        }

        let cont_can = document.getElementById("canvas" + num);
        charts = new Chart(cont_can, {
            type: 'bar',
            data: {
                labels: fechas,
                datasets: [
                    compras,
                    ventas,
                    ingresos,
                    consumos
                ]
            },
            plugins: [ChartDataLabels],
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                },
                distribution: 'linear',
                responsive: true,
                legend: {
                    display: true,
                    labels: {
                        fontColor: 'rgb(255, 99, 132)',
                        fontFamily: "'Arial', 'sans-serif'",
                        fontSize: 20
                    },
                },
                plugins: {
                    datalabels: {
                        labels: {
                            title: {
                                font: {
                                    weight: 'bold',
                                    size: 16
                                }
                            },
                        },
                        anchor: 'end',
                        align: 'top'
                    }
                }
            }
        })
    }

    // graficas_producto(3);

    $("#h1_info").hide();
    $("#h2_detalle").hide();
    $("#opc_1").hide();
    $("#opc_2").hide();
    $("#tabla_general").hide();
    $("#tabla_productos").hide();
    $("#t_detalles_prod").hide();
    
    const resetear_formulario = () => {
        $("#opc_1").hide();
        $("#opc_2").hide();
        $("form").trigger("reset");
    }
    
    $("input[name='opcion_vista']").click(function () {
        if($(this).val() == 'GENERAL') {
            $("#opc_1").show();
            $("input[type='submit']:first").attr("id", "enviar")
            $("input[type='submit']:last").removeAttr("id")
            $("input[type='submit']:first").removeAttr("disabled")
            $("input[type='submit']:last").attr("disabled")
            $("#opc_2").hide();
        } else{
            if ($(this).val() == 'producto') {
                $("#opc_1").hide();
                $("input[type='submit']:last").attr("id", "enviar");
                $("input[type='submit']:first").removeAttr("id");
                $("#enviar2").removeAttr("disabled");
                $("#enviar").attr("disabled");
                $("#opc_2").show();
            }
        }
    });

    var contador = 1;
    $("#contador").text(contador);
    $("#crear_form_producto").click(function () {
        
        if(contador < 3) {
            ++contador;
            $("#contador").text(contador);
            var otro_producto = $(".otro_producto:first").clone();
            otro_producto.addClass("otro_producto_copia");

            otro_producto.find("input[type='checkbox']").eq(0).removeAttr("id");
            otro_producto.find("input[type='checkbox']").eq(0).attr("id", "opc_compras" + contador);
            otro_producto.find("label").eq(0).removeAttr("for");
            otro_producto.find("label").eq(0).attr("for", "opc_compras" + contador);
            otro_producto.find("input[type='checkbox']").eq(1).removeAttr("id");
            otro_producto.find("input[type='checkbox']").eq(1).attr("id", "opc_ventas" + contador);
            otro_producto.find("label").eq(1).removeAttr("for");
            otro_producto.find("label").eq(1).attr("for", "opc_ventas" + contador);
            otro_producto.find("input[type='checkbox']").eq(2).removeAttr("id");
            otro_producto.find("input[type='checkbox']").eq(2).attr("id", "opc_otros" + contador);
            otro_producto.find("label").eq(2).removeAttr("for");
            otro_producto.find("label").eq(2).attr("for", "opc_otros" + contador);
            otro_producto.insertAfter(".otro_producto:last");
        }
    });
    
    $("#eliminar_form_producto").click(function () {
        if(!$(".otro_producto_copia")[0]) {
            contador = 1;
        } else {
            $(".otro_producto_copia").last().remove();
            contador--;
            $("#contador").text(contador);
        }
    });0

    $("#btn_cerrar_opc1").click(function () {
        var buscar_inputs = $(this).parent();
        buscar_inputs.find("input[type='radio']").prop("checked", false);
        buscar_inputs.hide();
        $("input[name='opcion_vista']").prop("checked", false);
    });
    $("#btn_cerrar_opc2").click(function () {
        var buscar_inputs = $(this).parent().parent();
        $(buscar_inputs).hide();
        if($(".otro_producto_copia")) {
            $(".otro_producto_copia").remove();
        }
        buscar_inputs.find("input[type='checkbox']").prop("checked", false);
        buscar_inputs.find("select").prop("selectedIndex", 0);
        $("input[name='opcion_vista']").prop("checked", false);
    });
    
    $("#limpiar").click(function () {
        limpiar_todo();
    });

    $("form").change(function () {
        $("#limpiar").removeAttr("disabled");
    });

    $("form").submit(function (e) {
        let $this = $(this);
        var valor_opcion = $("input[name='opcion_vista']:checked").val();
        var fecha_inicio = $("input[name='fecha_inicio']").val();
        var fecha_termino = $("input[name='fecha_termino']").val();

        if(fecha_inicio != "" && fecha_termino != "") {
            switch(valor_opcion) {
                case 'GENERAL':
                    var compras_sel = $("input[name='compra']").is(":checked");
                    var ventas_sel = $("input[name='venta']").is(":checked");
                    var otros_sel = $("input[name='otro_mov']").is(":checked");
                    
                    if(compras_sel || ventas_sel || otros_sel) {
                            $.ajax({
                                type: 'POST',
                                url: $("#enviar").attr("dato-ajax"),
                                data: $this.serializeArray(),
                                success: function (res) {
                                    var elemento = document.createElement("tr");
                                    $.map(res.datos[0], function (valor_dato, indexOrKey) {
                                        let campo_td = document.createElement("td");
                                        campo_td.innerText = valor_dato.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                                        elemento.appendChild(campo_td);
                                    });
                                    $("#response").append(elemento);
                                    $("#h1_info").hide();
                                    $("#tabla_general").show();
                                    resetear_formulario();
                                    
                                    const ventas = {
                                        label: "Ventas",
                                        data: res.c_ventas,
                                        backgroundColor: 'rgba(230, 8, 100, .4)', // Color de fondo
                                        borderColor: 'rgba(230, 8, 100, 1)', // Color del borde
                                        borderWidth: 3,// Ancho del borde
                                        tension: .5,
                                        fill: true,
                                    };
                                    const compras = {
                                        label: "Compras",
                                        data: res.c_compras, // La data es un arreglo que debe tener la misma cantidad de valores que la cantidad de etiquetas
                                        backgroundColor: 'rgba(151, 197, 199, .4)', // Color de fondo
                                        borderColor: 'rgba(151, 197, 199, 1)', // Color del borde
                                        borderWidth: 3,// Ancho del borde
                                        tension: .5,
                                        fill: true,
                                    };
                                    const ingresos = {
                                        label: "Ingresos",
                                        data: res.c_ingresos, 
                                        backgroundColor: 'rgba(22, 170, 133, .4)', // Color de fondo
                                        borderColor: 'rgba(22, 170, 133, 1)', // Color del borde
                                        borderWidth: 3,// Ancho del borde
                                        tension: .5,
                                        fill: true,
                                    };
                                    const consumos = {
                                        label: "Consumos",
                                        data: res.c_consumos,
                                        backgroundColor: 'rgba(218, 202, 58, .4)', // Color de fondo
                                        borderColor: 'rgba(218, 202, 58, 1)', // Color del borde
                                        borderWidth: 3,// Ancho del borde
                                        tension: .5,
                                        fill: true,
                                    };

                                    if(compras_sel && ventas_sel && otros_sel) {
                                        generar_grafica(res.fechas, compras, ventas, ingresos, consumos);
                                    } else if(compras_sel && ventas_sel) {
                                        generar_grafica(res.fechas, compras, ventas,);
                                    } else if(ventas_sel && otros_sel) {
                                        generar_grafica(res.fechas, undefined,ventas, ingresos, consumos);
                                    } else if(compras_sel && otros_sel) {
                                        generar_grafica(res.fechas, compras, undefined,ingresos, consumos);
                                    } else if(compras_sel) {
                                        generar_grafica(res.fechas, compras);
                                    } else if(ventas_sel) {
                                        generar_grafica(res.fechas, undefined,ventas);
                                    } else if(otros_sel) {
                                        generar_grafica(res.fechas, undefined, undefined, ingresos, consumos);
                                    }
                                }
                            });
                        }
                    else {
                        swal.fire({
                            position: 'center',
                            icon: 'warning',
                            title: 'Debe de elegir alguna de las 3 opciones',
                            showConfirmButton: false,
                            timer: 1500
                        })
                    }
                break;
                case 'producto':
                    $.ajax({
                        type: 'POST',
                        url: $("#enviar").attr("dato-ajax"),
                        data: $this.serializeArray(),
                        success: function (res) {
                            $.map(res.datos, function (valor_dato, indexOrKey) {
                                var elemento = document.createElement("tr");
                                for(let i = 0; i < valor_dato.length; i++) {
                                    let campo_td = document.createElement("td");
                                    campo_td.innerText = valor_dato[i];
                                    elemento.appendChild(campo_td);
                                }
                                $("#response2").append(elemento);
                            });

                            var num_ = 0;
                            $.each($("select.select_productos option:selected"), function () {
                                if(!$(this).is("disabled")) {
                                    let arreglo_compras_obt = [];
                                    let arreglo_ventas_obt = [];
                                    let arreglo_ingresos_obt = [];
                                    let arreglo_consumos_obt = [];
                                    let arreglo_fechas_obt = [];
                                    let fechas = [];

                                    for(let i = 0; i < res.productos[$(this).val()].length; i++) {
                                        var elemento_detalle = document.createElement("tr");
                                        for(let j = 0; j < res.productos[$(this).val()][i].length; j++) {
                                            var campo_td = document.createElement("td");
                                            campo_td.innerText = res.productos[$(this).val()][i][j];
                                            elemento_detalle.appendChild(campo_td);
                                        }
                                        $(".t_detalles_body").append(elemento_detalle);
                                        fechas.push(res.productos[$(this).val()][i][2]);
                                        if(arreglo_fechas_obt.includes(res.productos[$(this).val()][i][2]) === false) {
                                            arreglo_compras_obt.push(0);
                                            arreglo_ventas_obt.push(0);
                                            arreglo_ingresos_obt.push(0);
                                            arreglo_consumos_obt.push(0);
                                            arreglo_fechas_obt.push(res.productos[$(this).val()][i][2]);
                                        }
                                    }
                                    

                                    
                                    for(let index = 0; index < res.productos[$(this).val()].length; index++) {
                                        if(res.productos[$(this).val()][index][4] == 'compra' && arreglo_fechas_obt.indexOf(fechas[index]) !== -1) {
                                            arreglo_compras_obt[arreglo_fechas_obt.indexOf(fechas[index])] = res.productos[$(this).val()][index][3];
                                        }
                                        if(res.productos[$(this).val()][index][4] == 'venta' && arreglo_fechas_obt.indexOf(fechas[index]) !== -1) {
                                            arreglo_ventas_obt[arreglo_fechas_obt.indexOf(fechas[index])] = res.productos[$(this).val()][index][3];
                                        }
                                        if(res.productos[$(this).val()][index][4] == 'ingreso' && arreglo_fechas_obt.indexOf(fechas[index]) !== -1) {
                                            arreglo_ingresos_obt[arreglo_fechas_obt.indexOf(fechas[index])] = res.productos[$(this).val()][index][3];
                                        }
                                        if(res.productos[$(this).val()][index][4] == 'consumo' && arreglo_fechas_obt.indexOf(fechas[index]) !== -1) {
                                            arreglo_consumos_obt[arreglo_fechas_obt.indexOf(fechas[index])] = res.productos[$(this).val()][index][3];
                                        }
                                    }

                                    var cont_productos = Object.keys(res.productos).length;
                                    var ventas = {
                                        label: "Ventas",
                                        data: arreglo_ventas_obt, 
                                        backgroundColor: 'rgba(151, 197, 199, .4)', // Color de fondo
                                        borderColor: 'rgba(151, 197, 199, 1)', // Color del borde
                                        borderWidth: 3,// Ancho del borde
                                        tension: .5,
                                        fill: true,
                                    };
                                    var compras = {
                                        label: "Compras",
                                        data: arreglo_compras_obt, // La data es un arreglo que debe tener la misma cantidad de valores que la cantidad de etiquetas
                                        backgroundColor: 'rgba(230, 8, 100, .4)', // Color de fondo
                                        borderColor: 'rgba(230, 8, 100, 1)', // Color del borde
                                        borderWidth: 3,// Ancho del borde
                                        tension: .5,
                                        fill: true,
                                    };
                                    var ingresos = {
                                        label: "Ingresos",
                                        data: arreglo_ingresos_obt, 
                                        backgroundColor: 'rgba(22, 170, 133, .4)', // Color de fondo
                                        borderColor: 'rgba(22, 170, 133, 1)', // Color del borde
                                        borderWidth: 3,// Ancho del borde
                                        tension: .5,
                                        fill: true,
                                    };
                                    var consumos = {
                                        label: "Consumos",
                                        data: arreglo_consumos_obt,
                                        backgroundColor: 'rgba(218, 202, 58, .4)', // Color de fondo
                                        borderColor: 'rgba(218, 202, 58, 1)', // Color del borde
                                        borderWidth: 3,// Ancho del borde
                                        tension: .5,
                                        fill: true,
                                    };
                                    
                                    graficas_producto(++num_, arreglo_fechas_obt, compras, ventas, ingresos, consumos);
                                    for(let pro = 1; pro <= cont_productos; pro++) {
                                        $("#canvas" + pro).show();
                                    }
                                }
                            })
                            $("#h1_info").show();
                            $("#tabla_productos").show();
                            $("#h2_detalle").show();
                            $("#t_detalles_prod").show();
                            resetear_formulario();
                        }
                    });

                let arreglo_compras = [], arrelgo_ventas = [], arreglo_otros = [];
                $.each($("select.select_productos option:selected"),function (index) {
                    if(!$(this).is("disabled")) {
                        let panorama = $(this).parent().parent().parent().parent();
                        var ver_compra = panorama.find("input[name='ver_compras']");
                        var ver_venta = panorama.find("input[name='ver_ventas']");
                        var ver_otro = panorama.find("input[name='ver_otros']");
                        if (ver_compra.is(":checked")) {
                            arreglo_compras.push(ver_compra.val());
                        } else {
                            arreglo_compras.push('');
                        }
                        if (ver_venta.is(":checked")) {
                            arrelgo_ventas.push(ver_venta.val());
                        } else {
                            arrelgo_ventas.push('');
                        }
                        if (ver_otro.is(":checked")) {
                            arreglo_otros.push(ver_otro.val());
                        } else {
                            arreglo_otros.push('');
                        }
                    };
                });
                break;
                default:
                    swal.fire({
                        position: 'center',
                        icon: 'error',
                        title: 'No ha elegido opción entre General o Por producto',
                        showConfirmButton: false,
                        timer: 2000
                    })
                break;
            }
        }
        else {
            console.log("Fallo");
            swal.fire({
                position: 'center',
                icon: 'error',
                title: 'Debe elegir fecha de inicio y termino',
                showConfirmButton: false,
                timer: 2000
            })
        }
        e.preventDefault();
    });
});