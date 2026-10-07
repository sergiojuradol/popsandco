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

st.markdown("""
    <style>
    .stButton>button {
        transition: all 0.3s ease-in-out !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.15) !important;
    }
    [data-testid="stMetric"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; font-weight: 600 !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800 !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CATÁLOGO DE CUENTAS Y SUB-CUENTAS (PARCIALES)
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
# INICIALIZACIÓN DE ESTADOS (INVENTARIOS INICIALES EN CERO)
# ---------------------------------------------------------
if 'inventario_mp' not in st.session_state:
    st.session_state['inventario_mp'] = {
        "Maíz (kg)": {"cant": 0.0, "unidad": "kg", "costo_promedio": 0.0, "saldo_dinero": 0.0},
        "Aceite (L)": {"cant": 0.0, "unidad": "L", "costo_promedio": 0.0, "saldo_dinero": 0.0},
        "Flavacol (kg)": {"cant": 0.0, "unidad": "kg", "costo_promedio": 0.0, "saldo_dinero": 0.0},
        "Sazonador Cheddar (kg)": {"cant": 0.0, "unidad": "kg", "costo_promedio": 0.0, "saldo_dinero": 0.0},
        "Sazonador Queso Jalapeño (kg)": {"cant": 0.0, "unidad": "kg", "costo_promedio": 0.0, "saldo_dinero": 0.0},
        "Sazonador Habanero (kg)": {"cant": 0.0, "unidad": "kg", "costo_promedio": 0.0, "saldo_dinero": 0.0},
        "Sazonador Adobo (kg)": {"cant": 0.0, "unidad": "kg", "costo_promedio": 0.0, "saldo_dinero": 0.0},
    }

if 'inventario_indirectos' not in st.session_state:
    st.session_state['inventario_indirectos'] = {k: {"cant": 0, "unidad": "pzs", "costo_u": 0.0, "saldo_dinero": 0.0} for k in SUB_CUENTAS_INDIRECTOS}

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
    # Kárdex individual inicializado por cada insumo
    st.session_state['tarjetas_almacen_mp'] = {k: [] for k in SUB_CUENTAS_MP}

if 'tarjetas_almacen_ind' not in st.session_state:
    st.session_state['tarjetas_almacen_ind'] = {k: [] for k in SUB_CUENTAS_INDIRECTOS}

if 'libro_diario' not in st.session_state: st.session_state['libro_diario'] = []
if 'num_asiento' not in st.session_state: st.session_state['num_asiento'] = 1
if 'historial_lotes' not in st.session_state: st.session_state['historial_lotes'] = []
if 'historial_mermas' not in st.session_state: st.session_state['historial_mermas'] = []
if 'historial_ventas' not in st.session_state: st.session_state['historial_ventas'] = []

# ---------------------------------------------------------
# MENÚ LATERAL
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
    st.markdown("<h1 style='text-align: center; color: #E63946;'>🍿 POPS & CO 🍿</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555555; font-style: italic;'>« Sistema Contable Sincronizado en Tiempo Real »</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("💡 **Nota del Sistema:** Para habilitar existencias en el inventario de materia prima o empaques, debes registrar primero el **Asiento de Apertura** o un **Asiento de Compra** en la sección del **Libro Diario**.")

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
            "🛍️ Punto de Venta y Margen de Ganancia"
        ]
    )

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
            st.subheader("📜 Selecciona la Tarjeta de Almacén a Consultar")
            tipo_k = st.radio("Tipo de Almacén", ["Materia Prima Directa", "Material Indirecto / Empaques"], horizontal=True)
            
            if tipo_k == "Materia Prima Directa":
                ins_sel = st.selectbox("Selecciona Insumo", SUB_CUENTAS_MP)
                movs = st.session_state['tarjetas_almacen_mp'][ins_sel]
                if len(movs) > 0:
                    st.dataframe(pd.DataFrame(movs), use_container_width=True, hide_index=True)
                else:
                    st.info(f"Sin movimientos contables registrados para {ins_sel}.")
            else:
                ins_sel = st.selectbox("Selecciona Material", SUB_CUENTAS_INDIRECTOS)
                movs = st.session_state['tarjetas_almacen_ind'][ins_sel]
                if len(movs) > 0:
                    st.dataframe(pd.DataFrame(movs), use_container_width=True, hide_index=True)
                else:
                    st.info(f"Sin movimientos contables registrados para {ins_sel}.")

    elif subm_op == "📦 Inventario de Producto Terminado":
        st.header("📦 Inventario de Producto Terminado")
        filas_pt = [
            {"Sabor / Presentación": k, "Paquetes Disponibles": f"{v['cant']} pkts", "Precio Distribuidor": f"${v['precio_dist']:.2f}"}
            for k, v in st.session_state['inventario_pt'].items()
        ]
        st.dataframe(pd.DataFrame(filas_pt), use_container_width=True, hide_index=True)

    elif subm_op == "🏭 Registrar Lote de Producción y Costos":
        st.header("⚙️ Registro de Lote de Producción")
        st.caption("Al procesar el lote, el sistema consumirá de las existencias reales ingresadas mediante el Libro Diario.")
        
        up_trad = st.number_input("Tradicional (120g)", min_value=0, value=10)
        up_ched = st.number_input("Cheddar (120g)", min_value=0, value=10)
        
        if st.button("🚀 Procesar Lote de Producción"):
            # Validar si hay materia prima disponible
            cant_maiz = st.session_state['inventario_mp']['Maíz (kg)']['cant']
            if cant_maiz <= 0:
                st.error("❌ No hay Maíz en existencia. Primero debes registrar el Asiento de Apertura o una Compra en el Libro Diario.")
            else:
                st.session_state['inventario_pt']["Tradicional (120g)"]["cant"] += up_trad
                st.session_state['inventario_pt']["Cheddar (120g)"]["cant"] += up_ched
                st.balloons()
                st.success("✅ Lote registrado e inventario de PT actualizado.")

    elif subm_op == "🛍️ Punto de Venta y Margen de Ganancia":
        st.header("🛍️ Registro de Ventas")
        sabor_venta = st.selectbox("Selecciona Producto", list(st.session_state['inventario_pt'].keys()))
        cant_vender = st.number_input("Cantidad a vender", min_value=1, value=1)
        if st.button("💵 Confirmar Venta"):
            if st.session_state['inventario_pt'][sabor_venta]['cant'] >= cant_vender:
                st.session_state['inventario_pt'][sabor_venta]['cant'] -= cant_vender
                st.success("✅ Venta registrada exitosamente.")
            else:
                st.error("❌ Stock insuficiente en Producto Terminado.")

# ---------------------------------------------------------
# MÓDULO 2: CONTABILIDAD Y LIBRO DIARIO CON PARCIALES
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

    if subm_cont == "📖 Libro Diario con Parciales":
        st.header("📖 Libro Diario Contable con Sub-Cuentas (Parciales)")
        st.caption("Registra asientos compuestos integrando Parciales para actualizar tarjetas de almacén automáticamente.")

        if 'borrador_debe' not in st.session_state:
            st.session_state['borrador_debe'] = [{"Cuenta": CATALOGO_CUENTAS[3], "SubCuenta": SUB_CUENTAS_MP[0], "CantidadUds": 20.0, "Monto": 360.0}]
        if 'borrador_haber' not in st.session_state:
            st.session_state['borrador_haber'] = [{"Cuenta": CATALOGO_CUENTAS[12], "SubCuenta": "N/A", "CantidadUds": 0.0, "Monto": 360.0}]

        with st.expander("➕ Registrar Nuevo Asiento Contable", expanded=True):
            col_meta1, col_meta2 = st.columns([1, 3])
            f_asiento = col_meta1.date_input("Fecha", datetime.now())
            num_asiento_actual = col_meta1.number_input("Asiento #", value=int(st.session_state['num_asiento']), step=1)
            concepto_general = col_meta2.text_input("Concepto", value="Asiento de Apertura - Saldo Inicial en Almacén")

            st.markdown("---")
            col_d, col_h = st.columns(2)

            # --- DEBE ---
            with col_d:
                st.subheader("📥 DEBE (Cargos)")
                nuevas_debe = []
                for idx, item in enumerate(st.session_state['borrador_debe']):
                    st.markdown(f"**Partida #{idx+1}**")
                    cta = st.selectbox(f"Cuenta Debe #{idx+1}", CATALOGO_CUENTAS, index=CATALOGO_CUENTAS.index(item['Cuenta']) if item['Cuenta'] in CATALOGO_CUENTAS else 0, key=f"d_cta_{idx}")
                    
                    sub = "N/A"
                    uds = 0.0
                    if cta == "Almacén de materia prima":
                        sub = st.selectbox(f"Parcial / Insumo MP #{idx+1}", SUB_CUENTAS_MP, key=f"d_sub_{idx}")
                        uds = st.number_input(f"Cantidad Unidades (kg/L) #{idx+1}", min_value=0.0, value=float(item['CantidadUds']), key=f"d_uds_{idx}")
                    elif cta == "Almacén de material indirecto":
                        sub = st.selectbox(f"Parcial / Empaque #{idx+1}", SUB_CUENTAS_INDIRECTOS, key=f"d_sub_ind_{idx}")
                        uds = st.number_input(f"Cantidad Piezas #{idx+1}", min_value=0.0, value=float(item['CantidadUds']), key=f"d_uds_ind_{idx}")

                    monto = st.number_input(f"Monto DEBE $ #{idx+1}", min_value=0.0, value=float(item['Monto']), key=f"d_monto_{idx}")
                    nuevas_debe.append({"Cuenta": cta, "SubCuenta": sub, "CantidadUds": uds, "Monto": monto})

                st.session_state['borrador_debe'] = nuevas_debe
                if st.button("➕ Añadir Cargo (Debe)"):
                    st.session_state['borrador_debe'].append({"Cuenta": CATALOGO_CUENTAS[0], "SubCuenta": "N/A", "CantidadUds": 0.0, "Monto": 0.0})
                    st.rerun()

            # --- HABER ---
            with col_h:
                st.subheader("📤 HABER (Abonos)")
                nuevas_haber = []
                for idx, item in enumerate(st.session_state['borrador_haber']):
                    st.markdown(f"**Partida #{idx+1}**")
                    cta = st.selectbox(f"Cuenta Haber #{idx+1}", CATALOGO_CUENTAS, index=CATALOGO_CUENTAS.index(item['Cuenta']) if item['Cuenta'] in CATALOGO_CUENTAS else 12, key=f"h_cta_{idx}")
                    monto = st.number_input(f"Monto HABER $ #{idx+1}", min_value=0.0, value=float(item['Monto']), key=f"h_monto_{idx}")
                    nuevas_haber.append({"Cuenta": cta, "SubCuenta": "N/A", "CantidadUds": 0.0, "Monto": monto})

                st.session_state['borrador_haber'] = nuevas_haber
                if st.button("➕ Añadir Abono (Haber)"):
                    st.session_state['borrador_haber'].append({"Cuenta": CATALOGO_CUENTAS[12], "SubCuenta": "N/A", "CantidadUds": 0.0, "Monto": 0.0})
                    st.rerun()

            tot_d = sum(x['Monto'] for x in st.session_state['borrador_debe'])
            tot_h = sum(x['Monto'] for x in st.session_state['borrador_haber'])

            st.markdown("---")
            m1, m2 = st.columns(2)
            m1.metric("Total DEBE", f"${tot_d:,.2f}")
            m2.metric("Total HABER", f"${tot_h:,.2f}")

            if st.button("💾 Guardar Asiento y Actualizar Tarjetas de Almacén"):
                if round(abs(tot_d - tot_h), 2) != 0:
                    st.error("❌ La partida doble no cuadra.")
                elif tot_d == 0:
                    st.error("❌ Los montos deben ser mayores a $0.00.")
                else:
                    f_str = f_asiento.strftime("%Y-%m-%d")

                    # Process Cargos (Debe)
                    for d in st.session_state['borrador_debe']:
                        if d['Monto'] > 0:
                            st.session_state['libro_diario'].append({
                                "Asiento": num_asiento_actual, "Fecha": f_str, "Concepto": concepto_general,
                                "Cuenta Debe": d['Cuenta'], "Parcial (SubCuenta)": d['SubCuenta'],
                                "Debe": d['Monto'], "Cuenta Haber": "", "Haber": 0.0
                            })

                            # Actualización automática de Tarjeta de Almacén
                            if d['Cuenta'] == "Almacén de materia prima" and d['SubCuenta'] in SUB_CUENTAS_MP:
                                ins = d['SubCuenta']
                                cant_ingresada = d['CantidadUds']
                                monto_ingresado = d['Monto']
                                
                                curr_cant = st.session_state['inventario_mp'][ins]['cant']
                                curr_saldo = st.session_state['inventario_mp'][ins]['saldo_dinero']
                                
                                nueva_cant = curr_cant + cant_ingresada
                                nuevo_saldo = curr_saldo + monto_ingresado
                                nuevo_costo_prom = (nuevo_saldo / nueva_cant) if nueva_cant > 0 else 0.0

                                st.session_state['inventario_mp'][ins]['cant'] = nueva_cant
                                st.session_state['inventario_mp'][ins]['saldo_dinero'] = nuevo_saldo
                                st.session_state['inventario_mp'][ins]['costo_promedio'] = nuevo_costo_prom

                                st.session_state['tarjetas_almacen_mp'][ins].append({
                                    "Fecha": f_str, "Asiento": num_asiento_actual, "Concepto": concepto_general,
                                    "Entrada (Uds)": cant_ingresada, "Salida (Uds)": 0.0, "Existencia (Uds)": nueva_cant,
                                    "Costo Promedio": f"${nuevo_costo_prom:.2f}",
                                    "Debe ($)": f"${monto_ingresado:.2f}", "Haber ($)": "$0.00", "Saldo ($)": f"${nuevo_saldo:.2f}"
                                })

                            elif d['Cuenta'] == "Almacén de material indirecto" and d['SubCuenta'] in SUB_CUENTAS_INDIRECTOS:
                                mat = d['SubCuenta']
                                pzs_ingresadas = int(d['CantidadUds'])
                                monto_ingresado = d['Monto']

                                curr_cant = st.session_state['inventario_indirectos'][mat]['cant']
                                curr_saldo = st.session_state['inventario_indirectos'][mat]['saldo_dinero']

                                nueva_cant = curr_cant + pzs_ingresadas
                                nuevo_saldo = curr_saldo + monto_ingresado
                                nuevo_costo_u = (nuevo_saldo / nueva_cant) if nueva_cant > 0 else 0.0

                                st.session_state['inventario_indirectos'][mat]['cant'] = nueva_cant
                                st.session_state['inventario_indirectos'][mat]['saldo_dinero'] = nuevo_saldo
                                st.session_state['inventario_indirectos'][mat]['costo_u'] = nuevo_costo_u

                                st.session_state['tarjetas_almacen_ind'][mat].append({
                                    "Fecha": f_str, "Asiento": num_asiento_actual, "Concepto": concepto_general,
                                    "Entrada (Pzs)": pzs_ingresadas, "Salida (Pzs)": 0, "Existencia (Pzs)": nueva_cant,
                                    "Costo Unitario": f"${nuevo_costo_u:.2f}",
                                    "Debe ($)": f"${monto_ingresado:.2f}", "Haber ($)": "$0.00", "Saldo ($)": f"${nuevo_saldo:.2f}"
                                })

                    # Process Abonos (Haber)
                    for h in st.session_state['borrador_haber']:
                        if h['Monto'] > 0:
                            st.session_state['libro_diario'].append({
                                "Asiento": num_asiento_actual, "Fecha": f_str, "Concepto": concepto_general,
                                "Cuenta Debe": "", "Parcial (SubCuenta)": "", "Debe": 0.0,
                                "Cuenta Haber": h['Cuenta'], "Haber": h['Monto']
                            })

                    st.session_state['num_asiento'] += 1
                    st.session_state['borrador_debe'] = [{"Cuenta": CATALOGO_CUENTAS[0], "SubCuenta": "N/A", "CantidadUds": 0.0, "Monto": 0.0}]
                    st.session_state['borrador_haber'] = [{"Cuenta": CATALOGO_CUENTAS[12], "SubCuenta": "N/A", "CantidadUds": 0.0, "Monto": 0.0}]
                    st.success("✅ Asiento guardado. Tarjetas de almacén e inventarios actualizados en tiempo real.")
                    st.rerun()

        if len(st.session_state['libro_diario']) > 0:
            st.subheader("📜 Libro Diario Registrado")
            st.dataframe(pd.DataFrame(st.session_state['libro_diario']), use_container_width=True, hide_index=True)

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
                col1.dataframe(debes, use_container_width=True, hide_index=True)
                col2.dataframe(haberes, use_container_width=True, hide_index=True)
                
                tot_d = debes['Monto'].sum()
                tot_h = haberes['Monto'].sum()
                st.info(f"**Saldo:** ${abs(tot_d - tot_h):.2f} " + ("(Deudor)" if tot_d >= tot_h else "(Acreedor)"))
                st.markdown("---")

    elif subm_cont == "📈 Estado de Resultados":
        st.header("📈 Estado de Resultados")
        st.info("Visualización contable estándar en desarrollo.")

    elif subm_cont == "🏛️ Balance General":
        st.header("🏛️ Balance General")
        st.info("Visualización contable estándar en desarrollo.")
