import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL Y ESTILOS CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="POPS & CO - Sistema Integral Sincronizado",
    page_icon="🍿",
    layout="wide"
)

# Estilos CSS con corrección para Modo Oscuro y Animaciones
st.markdown("""
    <style>
    /* Transición suave para botones */
    .stButton>button {
        transition: all 0.3s ease-in-out !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Contraste y animación para tarjetas y métricas */
    [data-testid="stMetric"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    .element-container {
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CATÁLOGO OFICIAL DE CUENTAS Y SUB-CUENTAS (PARCIALES)
# ---------------------------------------------------------
CATALOGO_CUENTAS = [
    "Bancos", "Caja", "Clientes", "Almacén de materia prima",
    "Almacén de material indirecto", "Almacén de producto terminado", "Deudores diversos",
    "Mobiliario", "Maquinaria y Equipo de Fabricación",
    "Proveedores", "Acreedores Bancarios", "Acreedores Diversos",
    "Capital Social", "Utilidad del ejercicio", "Nómina Operativa",
    "Ventas", "Otros productos", "Costo de ventas",
    "Gastos de administración", "Gastos de venta", "Gastos financieros", "Honorarios a socios"
]

SUB_CUENTAS_MP = [
    "Maíz (kg)", "Aceite (L)", "Flavacol (kg)", 
    "Sazonador Cheddar (kg)", "Sazonador Queso Jalapeño (kg)", 
    "Sazonador Habanero (kg)", "Sazonador Adobo (kg)"
]

SUB_CUENTAS_INDIRECTOS = [
    "Bolsas Celofán 20x35 (pzs)", "Etiquetas 120g Tradicional (pzs)",
    "Etiquetas 120g Cheddar (pzs)", "Etiquetas 120g Queso Jalapeño (pzs)",
    "Etiquetas 120g Habanero (pzs)", "Etiquetas 120g Adobo (pzs)", "Etiquetas 65g (pzs)"
]

ACTIVO_CIRCULANTE = [
    "Bancos", "Caja", "Clientes", "Almacén de materia prima",
    "Almacén de material indirecto", "Almacén de producto terminado", "Deudores diversos"
]
ACTIVO_NO_CIRCULANTE = ["Mobiliario", "Maquinaria y Equipo de Fabricación"]
PASIVO_CORTO_PLAZO = ["Proveedores", "Acreedores Bancarios", "Acreedores Diversos"]

# ---------------------------------------------------------
# INICIALIZACIÓN DE ESTADOS (TODAS LAS EXISTENCIAS EN $0.00)
# ---------------------------------------------------------
if 'inventario_mp' not in st.session_state:
    st.session_state['inventario_mp'] = {
        k: {"cant": 0.0, "unidad": k.split("(")[1].replace(")", ""), "costo_promedio": 0.0, "saldo_dinero": 0.0}
        for k in SUB_CUENTAS_MP
    }

if 'inventario_indirectos' not in st.session_state:
    st.session_state['inventario_indirectos'] = {
        k: {"cant": 0, "unidad": "pzs", "costo_u": 0.0, "saldo_dinero": 0.0} 
        for k in SUB_CUENTAS_INDIRECTOS
    }

if 'inventario_pt' not in st.session_state:
    st.session_state['inventario_pt'] = {
        "Tradicional (120g)": {"cant": 0, "precio_dist": 14.00, "costo_directo_u": 5.20},
        "Cheddar (120g)": {"cant": 0, "precio_dist": 17.00, "costo_directo_u": 7.10},
        "Queso Jalapeño (120g)": {"cant": 0, "precio_dist": 17.00, "costo_directo_u": 7.05},
        "Habanero (120g)": {"cant": 0, "precio_dist": 17.00, "costo_directo_u": 7.25},
        "Adobado (120g)": {"cant": 0, "precio_dist": 17.00, "costo_directo_u": 7.05},
        "Pedido Especial (65g)": {"cant": 0, "precio_dist": 10.00, "costo_directo_u": 3.80},
    }

if 'tarjetas_almacen_mp' not in st.session_state:
    st.session_state['tarjetas_almacen_mp'] = {k: [] for k in SUB_CUENTAS_MP}

if 'tarjetas_almacen_ind' not in st.session_state:
    st.session_state['tarjetas_almacen_ind'] = {k: [] for k in SUB_CUENTAS_INDIRECTOS}

if 'libro_diario' not in st.session_state: st.session_state['libro_diario'] = []
if 'num_asiento' not in st.session_state: st.session_state['num_asiento'] = 1
if 'historial_lotes' not in st.session_state: st.session_state['historial_lotes'] = []
if 'historial_mermas' not in st.session_state: st.session_state['historial_mermas'] = []
if 'historial_ventas' not in st.session_state: st.session_state['historial_ventas'] = []

if 'num_filas_debe' not in st.session_state: st.session_state['num_filas_debe'] = 1
if 'num_filas_haber' not in st.session_state: st.session_state['num_filas_haber'] = 1

# ---------------------------------------------------------
# MENÚ LATERAL Y NAVEGACIÓN PRINCIPAL
# ---------------------------------------------------------
st.sidebar.title("🍿 POPS & CO")
modulo_principal = st.sidebar.selectbox(
    "Selecciona Módulo:",
    ["🏠 Inicio", "⚙️ MÓDULO 1: OPERATIVO / PRODUCCIÓN", "📊 MÓDULO 2: CONTABILIDAD"]
)

# ---------------------------------------------------------
# MÓDULO 0: INICIO
# ---------------------------------------------------------
if modulo_principal == "🏠 Inicio":
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        try:
            st.image("POPS & CO.png", use_column_width=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #E63946;'>🍿 POPS & CO 🍿</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #555555; font-style: italic;'>« De puñito en puñito sabe mejor »</h3>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("🚀 Control Integral del Sistema")
    col_a, col_b, col_c = st.columns(3)
    col_a.info("### ⚙️ Operativo y Producción\nExistencias físicas, lotes de producción y ventas.")
    col_b.success("### 📖 Libro Diario\nAsientos contables con parciales, partida doble y Kárdex automático.")
    col_c.warning("### 🏛️ Estados Financieros\nEstado de Resultados y Balance General síncronos.")

    st.info("💡 **Aviso Contable:** Las existencias de materia prima arrancan en $0.00. Para habilitar inventario en las tarjetas de almacén, debes registrar un **Asiento de Apertura** o una **Compra** en el Libro Diario.")

# ---------------------------------------------------------
# MÓDULO 1: OPERATIVO / PRODUCCIÓN
# ---------------------------------------------------------
elif modulo_principal == "⚙️ MÓDULO 1: OPERATIVO / PRODUCCIÓN":
    subm_op = st.sidebar.radio(
        "Secciones Operativas:",
        [
            "🌾 Materia Prima (Valuación y Kárdex)",
            "📦 Inventario de Producto Terminado",
            "🏭 Registrar Lote de Producción y Costos",
            "🛍️ Punto de Venta y Margen de Ganancia",
            "⚠️ Control de Mermas y Diferencias"
        ]
    )

    # 1.1 MATERIA PRIMA Y KÁRDEX
    if subm_op == "🌾 Materia Prima (Valuación y Kárdex)":
        st.header("🌾 Tarjetas de Almacén y Kárdex Individual de Insumos")
        
        tab1, tab2 = st.tabs(["📊 Stock y Valuación Actual", "📜 Tarjetas de Almacén (Kárdex)"])
        
        with tab1:
            st.subheader("Materia Prima Directa")
            filas_mp = []
            for k, v in st.session_state['inventario_mp'].items():
                filas_mp.append({
                    "Insumo / Sub-Cuenta": k,
                    "Existencia Física": f"{v['cant']:.2f} {v['unidad']}",
                    "Costo Promedio Unitario": f"${v['costo_promedio']:.2f}",
                    "Saldo Total ($)": f"${v['saldo_dinero']:.2f}"
                })
            st.dataframe(pd.DataFrame(filas_mp), use_container_width=True, hide_index=True)

            st.subheader("Material Indirecto y Empaques")
            filas_ind = []
            for k, v in st.session_state['inventario_indirectos'].items():
                filas_ind.append({
                    "Material": k,
                    "Existencia Física": f"{v['cant']} pzs",
                    "Costo Unitario": f"${v['costo_u']:.2f}",
                    "Saldo Total ($)": f"${v['saldo_dinero']:.2f}"
                })
            st.dataframe(pd.DataFrame(filas_ind), use_container_width=True, hide_index=True)

        with tab2:
            st.subheader("📜 Consulta de Tarjetas de Almacén Individuales")
            tipo_k = st.radio("Tipo de Almacén", ["Materia Prima Directa", "Material Indirecto / Empaques"], horizontal=True)
            
            if tipo_k == "Materia Prima Directa":
                ins_sel = st.selectbox("Selecciona Insumo", SUB_CUENTAS_MP)
                movs = st.session_state['tarjetas_almacen_mp'][ins_sel]
                if len(movs) > 0:
                    st.dataframe(pd.DataFrame(movs), use_container_width=True, hide_index=True)
                else:
                    st.info(f"Sin movimientos contables registrados en el Libro Diario para {ins_sel}.")
            else:
                ins_sel = st.selectbox("Selecciona Material", SUB_CUENTAS_INDIRECTOS)
                movs = st.session_state['tarjetas_almacen_ind'][ins_sel]
                if len(movs) > 0:
                    st.dataframe(pd.DataFrame(movs), use_container_width=True, hide_index=True)
                else:
                    st.info(f"Sin movimientos contables registrados en el Libro Diario para {ins_sel}.")

    # 1.2 INVENTARIO PRODUCTO TERMINADO
    elif subm_op == "📦 Inventario de Producto Terminado":
        st.header("📦 Inventario de Producto Terminado")
        st.caption("Consulta del stock listo para venta y ajuste directo de inventario.")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("📊 Stock Actual")
            filas_pt = []
            for k, v in st.session_state['inventario_pt'].items():
                filas_pt.append({
                    "Sabor / Presentación": k,
                    "Paquetes Disponibles": f"{v['cant']} pkts",
                    "Precio Distribuidor": f"${v['precio_dist']:.2f}",
                    "Costo Directo Estimado": f"${v.get('costo_directo_u', 0.0):.2f}"
                })
            st.dataframe(pd.DataFrame(filas_pt), use_container_width=True, hide_index=True)

        with col2:
            st.subheader("✏️ Ajuste / Mermas de PT")
            prod_ajuste = st.selectbox("Selecciona Producto", list(st.session_state['inventario_pt'].keys()))
            cant_actual = st.session_state['inventario_pt'][prod_ajuste]['cant']
            
            tipo_ajuste = st.radio("Acción", ["Restar (Merma)", "Sumar (Ajuste)"], horizontal=True)
            cant_cambio = st.number_input("Cantidad de Paquetes", min_value=1, value=1)
            motivo = st.text_input("Motivo", value="Bolsa abierta / Rotura")

            if st.button("Aplicar Ajuste"):
                if "Restar" in tipo_ajuste:
                    if cant_actual >= cant_cambio:
                        st.session_state['inventario_pt'][prod_ajuste]['cant'] -= cant_cambio
                        st.session_state['historial_mermas'].append({
                            "Concepto": f"Merma de PT ({prod_ajuste})",
                            "Cantidad": f"{cant_cambio} pkts",
                            "Detalle": motivo
                        })
                        st.warning(f"⚠️ Se descontaron {cant_cambio} pkts.")
                    else:
                        st.error("No puedes restar más de lo existente.")
                else:
                    st.session_state['inventario_pt'][prod_ajuste]['cant'] += cant_cambio
                    st.success(f"✅ Se agregaron {cant_cambio} pkts.")

    # 1.3 REGISTRAR LOTE DE PRODUCCIÓN Y COSTOS
    elif subm_op == "🏭 Registrar Lote de Producción y Costos":
        st.header("⚙️ Registro de Lote de Producción")
        
        st.subheader("1. Producción Planeada por Sabor")
        c1, c2, c3, c4, c5 = st.columns(5)
        up_trad = c1.number_input("Tradicional (120g)", min_value=0, value=20)
        up_ched = c2.number_input("Cheddar (120g)", min_value=0, value=20)
        up_qjal = c3.number_input("Queso Jalapeño (120g)", min_value=0, value=10)
        up_hab = c4.number_input("Habanero (120g)", min_value=0, value=10)
        up_ado = c5.number_input("Adobado (120g)", min_value=0, value=10)
        up_65g = st.number_input("Pedido Especial (65g)", min_value=0, value=0)

        total_pkts = up_trad + up_ched + up_qjal + up_hab + up_ado + up_65g

        st.markdown("---")
        st.subheader("2. Mano de Obra Directa (MOD) y Gas")
        col_m1, col_m2, col_g = st.columns(3)
        horas_mod = col_m1.number_input("Horas de Trabajo", min_value=0.0, value=2.0)
        costo_hora_mod = col_m2.number_input("Costo por Hora MOD ($)", min_value=0.0, value=60.0)
        costo_gas = col_g.number_input("Costo de Gas ($)", min_value=0.0, value=50.0)

        tot_mod = horas_mod * costo_hora_mod

        if st.button("🚀 Procesar Lote de Producción"):
            cant_maiz = st.session_state['inventario_mp']['Maíz (kg)']['cant']
            if cant_maiz <= 0:
                st.error("❌ No hay Maíz en stock. Registra primero una entrada en el Libro Diario.")
            elif total_pkts == 0:
                st.error("❌ Debes indicar al menos un paquete a producir.")
            else:
                st.session_state['inventario_pt']["Tradicional (120g)"]["cant"] += up_trad
                st.session_state['inventario_pt']["Cheddar (120g)"]["cant"] += up_ched
                st.session_state['inventario_pt']["Queso Jalapeño (120g)"]["cant"] += up_qjal
                st.session_state['inventario_pt']["Habanero (120g)"]["cant"] += up_hab
                st.session_state['inventario_pt']["Adobado (120g)"]["cant"] += up_ado
                st.session_state['inventario_pt']["Pedido Especial (65g)"]["cant"] += up_65g

                f_act = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state['historial_lotes'].append({
                    "Fecha": f_act, "Paquetes Producidos": total_pkts,
                    "Mano de Obra": f"${tot_mod:.2f}", "Gas": f"${costo_gas:.2f}"
                })
                st.balloons()
                st.success(f"✅ ¡Lote procesado exitosamente! Total producido: {total_pkts} pkts.")

    # 1.4 PUNTO DE VENTA
    elif subm_op == "🛍️ Punto de Venta y Margen de Ganancia":
        st.header("🛍️ Punto de Venta (Registro de Ventas)")
        sabor_venta = st.selectbox("Selecciona Producto", list(st.session_state['inventario_pt'].keys()))
        stock_disp = st.session_state['inventario_pt'][sabor_venta]['cant']
        precio_u = st.session_state['inventario_pt'][sabor_venta]['precio_dist']

        col_v1, col_v2 = st.columns(2)
        cant_vender = col_v1.number_input("Cantidad a vender", min_value=1, value=1)
        cliente = col_v2.text_input("Cliente", value="Distribuidor General")

        total_cobrar = cant_vender * precio_u
        st.markdown(f"### Total a Cobrar: **${total_cobrar:.2f}**")

        if st.button("💵 Confirmar Venta"):
            if stock_disp >= cant_vender:
                st.session_state['inventario_pt'][sabor_venta]['cant'] -= cant_vender
                st.session_state['historial_ventas'].append({
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Cliente": cliente, "Producto": sabor_venta,
                    "Cantidad": cant_vender, "Total Cobrado": f"${total_cobrar:.2f}"
                })
                st.success("✅ Venta registrada correctamente.")
            else:
                st.error("❌ Stock insuficiente en Producto Terminado.")

    # 1.5 MERMAS
    elif subm_op == "⚠️ Control de Mermas y Diferencias":
        st.header("📋 Historial de Mermas y Desperdicios")
        if len(st.session_state['historial_mermas']) > 0:
            st.dataframe(pd.DataFrame(st.session_state['historial_mermas']), use_container_width=True, hide_index=True)
        else:
            st.info("👌 No hay mermas registradas.")

# ---------------------------------------------------------
# MÓDULO 2: CONTABILIDAD
# ---------------------------------------------------------
elif modulo_principal == "📊 MÓDULO 2: CONTABILIDAD":
    subm_cont = st.sidebar.radio(
        "Secciones Contables:",
        [
            "📖 Libro Diario con Parciales",
            "⚖️ Cuentas T (Esquemas de Mayor)",
            "📈 Estado de Resultados",
            "🏛️ Balance General"
        ]
    )

    # 2.1 LIBRO DIARIO CON FORMULARIO SEGURO
    if subm_cont == "📖 Libro Diario con Parciales":
        st.header("📖 Libro Diario Contable con Parciales")
        st.caption("Los cargos a cuentas de Almacén actualizan en tiempo real las Tarjetas de Almacén (Kárdex).")

        with st.form("form_libro_diario_multicuentas", clear_on_submit=True):
            col_m1, col_m2 = st.columns([1, 3])
            f_asiento = col_m1.date_input("Fecha del Asiento", datetime.now())
            num_asiento_actual = col_m1.number_input("Asiento #", value=int(st.session_state['num_asiento']), step=1)
            concepto_general = col_m2.text_input("Concepto / Descripción General", value="Asiento de Apertura - Saldos Iniciales")

            st.markdown("---")
            col_debe, col_haber = st.columns(2)

            # CARGOS (DEBE)
            entradas_debe = []
            with col_debe:
                st.subheader("📥 DEBE (Cargos)")
                for i in range(st.session_state['num_filas_debe']):
                    st.markdown(f"**Partida #{i+1}**")
                    cta = st.selectbox(f"Cuenta Debe #{i+1}", CATALOGO_CUENTAS, index=3 if i==0 else 0, key=f"f_debe_cta_{i}")
                    
                    sub = "N/A"
                    uds = 0.0
                    if cta == "Almacén de materia prima":
                        sub = st.selectbox(f"Insumo MP #{i+1}", SUB_CUENTAS_MP, key=f"f_debe_sub_mp_{i}")
                        uds = st.number_input(f"Cantidad (kg/L) #{i+1}", min_value=0.0, value=20.0 if i==0 else 0.0, key=f"f_debe_uds_mp_{i}")
                    elif cta == "Almacén de material indirecto":
                        sub = st.selectbox(f"Empaque #{i+1}", SUB_CUENTAS_INDIRECTOS, key=f"f_debe_sub_ind_{i}")
                        uds = st.number_input(f"Cantidad (Pzs) #{i+1}", min_value=0.0, value=100.0 if i==0 else 0.0, key=f"f_debe_uds_ind_{i}")

                    monto = st.number_input(f"Monto DEBE $ #{i+1}", min_value=0.0, value=360.0 if i==0 else 0.0, key=f"f_debe_monto_{i}")
                    entradas_debe.append({"Cuenta": cta, "SubCuenta": sub, "CantidadUds": uds, "Monto": monto})

            # ABONOS (HABER)
            entradas_haber = []
            with col_haber:
                st.subheader("📤 HABER (Abonos)")
                for i in range(st.session_state['num_filas_haber']):
                    st.markdown(f"**Partida #{i+1}**")
                    cta = st.selectbox(f"Cuenta Haber #{i+1}", CATALOGO_CUENTAS, index=12 if i==0 else 0, key=f"f_haber_cta_{i}")
                    monto = st.number_input(f"Monto HABER $ #{i+1}", min_value=0.0, value=360.0 if i==0 else 0.0, key=f"f_haber_monto_{i}")
                    entradas_haber.append({"Cuenta": cta, "SubCuenta": "N/A", "CantidadUds": 0.0, "Monto": monto})

            st.markdown("---")
            btn_guardar = st.form_submit_button("💾 Guardar y Procesar Asiento en Libro Diario")

        # Botones de ajuste dinámico de filas
        c_b1, c_b2, c_b3, c_b4 = st.columns(4)
        if c_b1.button("➕ Agregar Fila Debe"):
            st.session_state['num_filas_debe'] += 1
            st.rerun()
        if c_b2.button("➖ Quitar Fila Debe") and st.session_state['num_filas_debe'] > 1:
            st.session_state['num_filas_debe'] -= 1
            st.rerun()
        if c_b3.button("➕ Agregar Fila Haber"):
            st.session_state['num_filas_haber'] += 1
            st.rerun()
        if c_b4.button("➖ Quitar Fila Haber") and st.session_state['num_filas_haber'] > 1:
            st.session_state['num_filas_haber'] -= 1
            st.rerun()

        # Guardado del Asiento
        if btn_guardar:
            tot_d = sum(x['Monto'] for x in entradas_debe)
            tot_h = sum(x['Monto'] for x in entradas_haber)

            if round(abs(tot_d - tot_h), 2) != 0:
                st.error(f"❌ La partida doble no cuadra. Total DEBE: ${tot_d:,.2f} \vert{} Total HABER:${tot_h:,.2f}")
            elif tot_d == 0:
                st.error("❌ Los montos deben ser mayores a $0.00.")
            else:
                f_str = f_asiento.strftime("%Y-%m-%d")

                # Procesar Cargos
                for d in entradas_debe:
                    if d['Monto'] > 0:
                        st.session_state['libro_diario'].append({
                            "Asiento": num_asiento_actual, "Fecha": f_str, "Concepto": concepto_general,
                            "Cuenta Debe": d['Cuenta'], "Parcial (SubCuenta)": d['SubCuenta'],
                            "Debe": d['Monto'], "Cuenta Haber": "", "Haber": 0.0
                        })

                        # Kárdex MP
                        if d['Cuenta'] == "Almacén de materia prima" and d['SubCuenta'] in SUB_CUENTAS_MP:
                            ins = d['SubCuenta']
                            cant_in = d['CantidadUds']
                            monto_in = d['Monto']

                            curr = st.session_state['inventario_mp'][ins]
                            n_cant = curr['cant'] + cant_in
                            n_saldo = curr['saldo_dinero'] + monto_in
                            n_prom = (n_saldo / n_cant) if n_cant > 0 else 0.0

                            st.session_state['inventario_mp'][ins] = {
                                "cant": n_cant, "unidad": curr['unidad'],
                                "costo_promedio": n_prom, "saldo_dinero": n_saldo
                            }

                            st.session_state['tarjetas_almacen_mp'][ins].append({
                                "Fecha": f_str, "Asiento": num_asiento_actual, "Concepto": concepto_general,
                                "Entrada": cant_in, "Salida": 0.0, "Existencia": n_cant,
                                "Costo Promedio": f"${n_prom:.2f}",
                                "Debe ($)": f"${monto_in:.2f}", "Haber ($)": "$0.00", "Saldo ($)": f"${n_saldo:.2f}"
                            })

                        # Kárdex Empaques
                        elif d['Cuenta'] == "Almacén de material indirecto" and d['SubCuenta'] in SUB_CUENTAS_INDIRECTOS:
                            mat = d['SubCuenta']
                            pzs_in = int(d['CantidadUds'])
                            monto_in = d['Monto']

                            curr = st.session_state['inventario_indirectos'][mat]
                            n_cant = curr['cant'] + pzs_in
                            n_saldo = curr['saldo_dinero'] + monto_in
                            n_cu = (n_saldo / n_cant) if n_cant > 0 else 0.0

                            st.session_state['inventario_indirectos'][mat] = {
                                "cant": n_cant, "unidad": "pzs",
                                "costo_u": n_cu, "saldo_dinero": n_saldo
                            }

                            st.session_state['tarjetas_almacen_ind'][mat].append({
                                "Fecha": f_str, "Asiento": num_asiento_actual, "Concepto": concepto_general,
                                "Entrada": pzs_in, "Salida": 0, "Existencia": n_cant,
                                "Costo Unitario": f"${n_cu:.2f}",
                                "Debe ($)": f"${monto_in:.2f}", "Haber ($)": "$0.00", "Saldo ($)": f"${n_saldo:.2f}"
                            })

                # Procesar Abonos
                for h in entradas_haber:
                    if h['Monto'] > 0:
                        st.session_state['libro_diario'].append({
                            "Asiento": num_asiento_actual, "Fecha": f_str, "Concepto": concepto_general,
                            "Cuenta Debe": "", "Parcial (SubCuenta)": "", "Debe": 0.0,
                            "Cuenta Haber": h['Cuenta'], "Haber": h['Monto']
                        })

                st.session_state['num_asiento'] += 1
                st.session_state['num_filas_debe'] = 1
                st.session_state['num_filas_haber'] = 1
                st.success("✅ Asiento guardado. Tarjetas de almacén e inventarios actualizados en tiempo real.")
                st.rerun()

        if len(st.session_state['libro_diario']) > 0:
            st.subheader("📜 Libro Diario Registrado")
            st.dataframe(pd.DataFrame(st.session_state['libro_diario']), use_container_width=True, hide_index=True)

    # 2.2 CUENTAS T
    elif subm_cont == "⚖️ Cuentas T (Esquemas de Mayor)":
        st.header("⚖️ Cuentas T (Esquemas de Mayor)")
        if len(st.session_state['libro_diario']) > 0:
            df_diario = pd.DataFrame(st.session_state['libro_diario'])
            cuentas_usadas = sorted(list(set(df_diario['Cuenta Debe']).union(set(df_diario['Cuenta Haber'])) - {""}))

            for cuenta in cuentas_usadas:
                st.markdown(f"### 🏦 Cuenta: `{cuenta}`")
                debes = df_diario[df_diario['Cuenta Debe'] == cuenta][['Asiento', 'Debe']].rename(columns={'Debe': 'Monto'})
                haberes = df_diario[df_diario['Cuenta Haber'] == cuenta][['Asiento', 'Haber']].rename(columns={'Haber': 'Monto'})

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**DEBE (Cargos)**")
                    st.dataframe(debes, use_container_width=True, hide_index=True)
                with col2:
                    st.markdown("**HABER (Abonos)**")
                    st.dataframe(haberes, use_container_width=True, hide_index=True)

                tot_d = debes['Monto'].sum()
                tot_h = haberes['Monto'].sum()
                st.info(f"**Saldo:** ${abs(tot_d - tot_h):,.2f} " + ("(Deudor)" if tot_d >= tot_h else "(Acreedor)"))
                st.markdown("---")
        else:
            st.info("No hay asientos registrados en el Libro Diario.")

    # 2.3 ESTADO DE RESULTADOS
    elif subm_cont == "📈 Estado de Resultados":
        st.header("📈 Estado de Resultados (Mensual)")
        ventas = 0.0
        costo_ventas = 0.0
        gastos_admin = 0.0
        gastos_venta = 0.0

        if len(st.session_state['libro_diario']) > 0:
            df = pd.DataFrame(st.session_state['libro_diario'])
            ventas = df[df['Cuenta Haber'] == 'Ventas']['Haber'].sum()
            costo_ventas = df[df['Cuenta Debe'] == 'Costo de ventas']['Debe'].sum()
            gastos_admin = df[df['Cuenta Debe'] == 'Gastos de administración']['Debe'].sum()
            gastos_venta = df[df['Cuenta Debe'] == 'Gastos de venta']['Debe'].sum()

        utilidad_bruta = ventas - costo_ventas
        utilidad_op = utilidad_bruta - (gastos_admin + gastos_venta)

        st.metric("Ventas Totales", f"${ventas:,.2f}")
        st.metric("Costo de Ventas", f"${costo_ventas:,.2f}")
        st.metric("Utilidad Bruta", f"${utilidad_bruta:,.2f}")
        st.metric("Utilidad del Ejercicio", f"${utilidad_op:,.2f}")

    # 2.4 BALANCE GENERAL
    elif subm_cont == "🏛️ Balance General":
        st.header("🏛️ Balance General (Estado de Situación Financiera)")
        saldos = {cuenta: 0.0 for cuenta in CATALOGO_CUENTAS}
        if len(st.session_state['libro_diario']) > 0:
            for mov in st.session_state['libro_diario']:
                saldos[mov['Cuenta Debe']] += mov['Debe']
                saldos[mov['Cuenta Haber']] -= mov['Haber']

        tot_circulante = sum(saldos[c] for c in ACTIVO_CIRCULANTE if c in saldos)
        tot_no_circulante = sum(saldos[c] for c in ACTIVO_NO_CIRCULANTE if c in saldos)
        tot_activo = tot_circulante + tot_no_circulante

        tot_pasivo = abs(sum(saldos[c] for c in PASIVO_CORTO_PLAZO if c in saldos))
        capital_social = abs(saldos.get("Capital Social", 0.0))
        tot_capital = capital_social
        tot_pasivo_capital = tot_pasivo + tot_capital

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("ACTIVO")
            st.write(f"**Circulante:** ${tot_circulante:,.2f}")
            st.write(f"**No Circulante:** ${tot_no_circulante:,.2f}")
            st.markdown(f"### **TOTAL ACTIVO:** `${tot_activo:,.2f}`")

        with col2:
            st.subheader("PASIVO Y CAPITAL")
            st.write(f"**Pasivo Corto Plazo:** ${tot_pasivo:,.2f}")
            st.write(f"**Capital Social:** ${capital_social:,.2f}")
            st.markdown(f"### **TOTAL PASIVO + CAPITAL:** `${tot_pasivo_capital:,.2f}`")

        st.markdown("---")
        if abs(tot_activo - tot_pasivo_capital) < 0.01:
            st.success("⚖️ ¡El Balance General está perfectamente cuadrado!")
        else:
            st.warning(f"⚠️ El Balance General presenta una diferencia de ${abs(tot_activo - tot_pasivo_capital):,.2f}")
