import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL Y ESTILOS CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="POPS & CO - Sistema Contable Completo",
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
# CATÁLOGO DE CUENTAS Y SUB-CUENTAS
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
# INICIALIZACIÓN ROBUSTA DE ESTADOS EN SESSION_STATE
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

if 'num_filas_debe' not in st.session_state: st.session_state['num_filas_debe'] = 1
if 'num_filas_haber' not in st.session_state: st.session_state['num_filas_haber'] = 1

# ---------------------------------------------------------
# MENÚ LATERAL Y NAVEGACIÓN
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
    st.markdown("<h3 style='text-align: center; color: #555555; font-style: italic;'>« Sistema Contable Sincronizado »</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("💡 **Recordatorio Contable:** El inventario inicial inicia en $0.00. Para ingresar existencias a los almacenes, debes registrar el **Asiento de Apertura** o una compra en el Libro Diario.")

# ---------------------------------------------------------
# MÓDULO 1: OPERATIVO / PRODUCCIÓN
# ---------------------------------------------------------
elif modulo_principal == "⚙️ MÓDULO 1: OPERATIVO / PRODUCCIÓN":
    subm_op = st.sidebar.radio(
        "Secciones Operativas:",
        [
            "🌾 Materia Prima (Valuación y Kárdex)",
            "📦 Inventario de Producto Terminado",
            "🏭 Registrar Lote de Producción"
        ]
    )

    if subm_op == "🌾 Materia Prima (Valuación y Kárdex)":
        st.header("🌾 Tarjetas de Almacén y Kárdex Individual")
        
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
            st.subheader("📜 Consulta de Tarjetas de Almacén")
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

    elif subm_op == "🏭 Registrar Lote de Producción":
        st.header("⚙️ Registro de Lote de Producción")
        up_trad = st.number_input("Tradicional (120g)", min_value=0, value=10)
        up_ched = st.number_input("Cheddar (120g)", min_value=0, value=10)
        
        if st.button("🚀 Procesar Lote"):
            cant_maiz = st.session_state['inventario_mp']['Maíz (kg)']['cant']
            if cant_maiz <= 0:
                st.error("❌ No hay Maíz suficiente en stock. Debes registrar una entrada primero en el Libro Diario.")
            else:
                st.session_state['inventario_pt']["Tradicional (120g)"]["cant"] += up_trad
                st.session_state['inventario_pt']["Cheddar (120g)"]["cant"] += up_ched
                st.balloons()
                st.success("✅ Lote registrado en inventario.")

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

    if subm_cont == "📖 Libro Diario con Parciales":
        st.header("📖 Libro Diario Contable con Parciales")
        st.caption("Captura de asientos con desglose de subcuentas para actualizar las Tarjetas de Almacén.")

        with st.form("form_asiento_contable", clear_on_submit=True):
            col_meta1, col_meta2 = st.columns([1, 3])
            f_asiento = col_meta1.date_input("Fecha", datetime.now())
            num_asiento_actual = col_meta1.number_input("Asiento #", value=int(st.session_state['num_asiento']), step=1)
            concepto_general = col_meta2.text_input("Concepto General", value="Asiento de Apertura - Saldo Inicial")

            st.markdown("---")
            col_debe, col_haber = st.columns(2)

            # DEBE (CARGOS)
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

            # HABER (ABONOS)
            entradas_haber = []
            with col_haber:
                st.subheader("📤 HABER (Abonos)")
                for i in range(st.session_state['num_filas_haber']):
                    st.markdown(f"**Partida #{i+1}**")
                    cta = st.selectbox(f"Cuenta Haber #{i+1}", CATALOGO_CUENTAS, index=12 if i==0 else 0, key=f"f_haber_cta_{i}")
                    monto = st.number_input(f"Monto HABER $ #{i+1}", min_value=0.0, value=360.0 if i==0 else 0.0, key=f"f_haber_monto_{i}")
                    entradas_haber.append({"Cuenta": cta, "SubCuenta": "N/A", "CantidadUds": 0.0, "Monto": monto})

            st.markdown("---")
            btn_guardar = st.form_submit_button("💾 Guardar y Procesar Asiento Contable")

        # Botones fuera del formulario para añadir/quitar filas
        c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)
        if c_btn1.button("➕ Agregar Fila Debe"):
            st.session_state['num_filas_debe'] += 1
            st.rerun()
        if c_btn2.button("➖ Quitar Fila Debe") and st.session_state['num_filas_debe'] > 1:
            st.session_state['num_filas_debe'] -= 1
            st.rerun()
        if c_btn3.button("➕ Agregar Fila Haber"):
            st.session_state['num_filas_haber'] += 1
            st.rerun()
        if c_btn4.button("➖ Quitar Fila Haber") and st.session_state['num_filas_haber'] > 1:
            st.session_state['num_filas_haber'] -= 1
            st.rerun()

        # Procesamiento al presionar el botón del formulario
        if btn_guardar:
            tot_d = sum(x['Monto'] for x in entradas_debe)
            tot_h = sum(x['Monto'] for x in entradas_haber)

            if round(abs(tot_d - tot_h), 2) != 0:
                st.error(f"❌ La partida doble no cuadra. Total Debe: ${tot_d:.2f} \vert{} Total Haber:${tot_h:.2f}")
            elif tot_d == 0:
                st.error("❌ Los montos deben ser mayores a $0.00.")
            else:
                f_str = f_asiento.strftime("%Y-%m-%d")

                # Procesar Debe
                for d in entradas_debe:
                    if d['Monto'] > 0:
                        st.session_state['libro_diario'].append({
                            "Asiento": num_asiento_actual, "Fecha": f_str, "Concepto": concepto_general,
                            "Cuenta Debe": d['Cuenta'], "Parcial (SubCuenta)": d['SubCuenta'],
                            "Debe": d['Monto'], "Cuenta Haber": "", "Haber": 0.0
                        })

                        # Actualizar Kárdex MP
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

                        # Actualizar Kárdex Empaques
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

                # Procesar Haber
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
                st.success("✅ Asiento guardado correctamente. Tarjetas de almacén e inventarios actualizados.")
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

        st.metric("Ventas Totales", f"${ventas:.2f}")
        st.metric("Costo de Ventas", f"${costo_ventas:.2f}")
        st.metric("Utilidad Bruta", f"${utilidad_bruta:.2f}")
        st.metric("Utilidad del Ejercicio", f"${utilidad_op:.2f}")

    elif subm_cont == "🏛️ Balance General":
        st.header("🏛️ Balance General")
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
        col1.write(f"### **TOTAL ACTIVO:** ${tot_activo:.2f}")
        col2.write(f"### **TOTAL PASIVO + CAPITAL:** ${tot_pasivo_capital:.2f}")
