import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURACIÓN INICIAL Y ESTILOS / ANIMACIONES CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="POPS & CO - Sistema Integral",
    page_icon="🍿",
    layout="wide"
)

# Estilos CSS personalizados para animaciones y transiciones
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
    
    /* Animación de entrada para tarjetas / metris */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
    }

    /* Animación de desvanecimiento suave para contenedores */
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
# CATÁLOGO OFICIAL DE CUENTAS CONTABLES
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

ACTIVO_CIRCULANTE = [
    "Bancos", "Caja", "Clientes", "Almacén de materia prima",
    "Almacén de material indirecto", "Almacén de producto terminado", "Deudores diversos"
]
ACTIVO_NO_CIRCULANTE = ["Mobiliario", "Maquinaria y Equipo de Fabricación"]
PASIVO_CORTO_PLAZO = ["Proveedores", "Acreedores Bancarios", "Acreedores Diversos"]

# ---------------------------------------------------------
# INICIALIZACIÓN DE ESTADOS (MEMORIA TEMPORAL)
# ---------------------------------------------------------
if 'inventario_mp' not in st.session_state:
    st.session_state['inventario_mp'] = {
        "Maíz": {"cant_kg": 20.0, "costo_promedio_kg": 18.00},
        "Aceite": {"cant_l": 10.0, "costo_promedio_l": 37.50},
        "Flavacol": {"cant_g": 1000.0, "costo_promedio_kg": 130.00},
        "Sazonador Cheddar": {"cant_g": 1000.0, "costo_promedio_kg": 160.00},
        "Sazonador Queso Jalapeño": {"cant_g": 1000.0, "costo_promedio_kg": 155.00},
        "Sazonador Habanero": {"cant_g": 1000.0, "costo_promedio_kg": 175.00},
        "Sazonador Adobo": {"cant_g": 1000.0, "costo_promedio_kg": 155.00},
    }

if 'inventario_indirectos' not in st.session_state:
    st.session_state['inventario_indirectos'] = {
        "Bolsas Celofán 20x35 (pzs)": {"cant": 2000, "costo_u": 0.40},
        "Etiquetas 120g Tradicional (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Cheddar (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Queso Jalapeño (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Habanero (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 120g Adobo (pzs)": {"cant": 500, "costo_u": 1.75},
        "Etiquetas 65g (pzs)": {"cant": 200, "costo_u": 1.25},
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

if 'historial_movimientos_mp' not in st.session_state:
    f_apertura = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state['historial_movimientos_mp'] = [
        {"Fecha": f_apertura, "Insumo": "Maíz", "Tipo": "Entrada Inicial", "Cantidad": "20.0 kg", "Detalle": "Inventario inicial de apertura"},
        {"Fecha": f_apertura, "Insumo": "Aceite", "Tipo": "Entrada Inicial", "Cantidad": "10.0 L", "Detalle": "Inventario inicial de apertura"},
    ]

if 'historial_mermas' not in st.session_state: st.session_state['historial_mermas'] = []
if 'historial_ventas' not in st.session_state: st.session_state['historial_ventas'] = []
if 'historial_lotes' not in st.session_state: st.session_state['historial_lotes'] = []
if 'libro_diario' not in st.session_state: st.session_state['libro_diario'] = []
if 'num_asiento' not in st.session_state: st.session_state['num_asiento'] = 1

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
    st.markdown("<h3 style='text-align: center; color: #555555; font-style: italic;'>« De puñito en puñito sabe mejor »</h3>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("🚀 Control del Sistema")
    col_a, col_b, col_c = st.columns(3)
    col_a.info("### ⚙️ Operativo y Producción\nExistencias, lotes de fabricación y ventas físicas.")
    col_b.success("### 📖 Libro Diario\nAsientos contables, partida doble y cuentas T.")
    col_c.warning("### 🏛️ Estados Financieros\nEstado de Resultados y Balance General.")

# ---------------------------------------------------------
# MÓDULO 1: OPERATIVO
# ---------------------------------------------------------
elif modulo_principal == "⚙️ MÓDULO 1: OPERATIVO / PRODUCCIÓN":
    subm_op = st.sidebar.radio(
        "Secciones Operativas:",
        [
            "📦 Inventario de Producto Terminado",
            "🌾 Materia Prima (Físico y Movimientos)",
            "🏭 Registrar Lote de Producción y Costos",
            "🛍️ Punto de Venta y Margen de Ganancia"
        ]
    )

    if subm_op == "📦 Inventario de Producto Terminado":
        st.header("📦 Inventario de Producto Terminado")
        filas_pt = [
            {"Sabor / Presentación": k, "Paquetes Disponibles": f"{v['cant']} pkts", "Precio Distribuidor": f"${v['precio_dist']:.2f}"}
            for k, v in st.session_state['inventario_pt'].items()
        ]
        st.dataframe(pd.DataFrame(filas_pt), use_container_width=True, hide_index=True)

    elif subm_op == "🌾 Materia Prima (Físico y Movimientos)":
        st.header("🌾 Materia Prima e Insumos")
        filas_mp = []
        for k, v in st.session_state['inventario_mp'].items():
            cant_str = f"{v.get('cant_kg', v.get('cant_l', v.get('cant_g', 0)))} " + ("kg" if "cant_kg" in v else "L" if "cant_l" in v else "g")
            filas_mp.append({"Insumo": k, "Stock": cant_str})
        st.dataframe(pd.DataFrame(filas_mp), use_container_width=True, hide_index=True)

    elif subm_op == "🏭 Registrar Lote de Producción y Costos":
        st.header("⚙️ Registro de Lote de Producción")
        up_trad = st.number_input("Tradicional (120g)", min_value=0, value=40)
        up_ched = st.number_input("Cheddar (120g)", min_value=0, value=65)
        total_pkts = up_trad + up_ched
        if st.button("🚀 Procesar Lote"):
            st.session_state['inventario_pt']["Tradicional (120g)"]["cant"] += up_trad
            st.session_state['inventario_pt']["Cheddar (120g)"]["cant"] += up_ched
            st.balloons()
            st.success(f"✅ ¡Lote Procesado! Total paquetes: {total_pkts}")

    elif subm_op == "🛍️ Punto de Venta y Margen de Ganancia":
        st.header("🛍️ Registro de Ventas")
        sabor_venta = st.selectbox("Selecciona Producto", list(st.session_state['inventario_pt'].keys()))
        cant_vender = st.number_input("Cantidad a vender", min_value=1, value=5)
        if st.button("💵 Confirmar Venta"):
            if st.session_state['inventario_pt'][sabor_venta]['cant'] >= cant_vender:
                st.session_state['inventario_pt'][sabor_venta]['cant'] -= cant_vender
                st.success("✅ Venta registrada exitosamente.")
            else:
                st.error("❌ Stock insuficiente.")

# ---------------------------------------------------------
# MÓDULO 2: CONTABILIDAD
# ---------------------------------------------------------
elif modulo_principal == "📊 MÓDULO 2: CONTABILIDAD":
    subm_cont = st.sidebar.radio(
        "Secciones Contables:",
        [
            "📖 Libro Diario",
            "⚖️ Cuentas T (Esquemas de Mayor)",
            "📈 Estado de Resultados",
            "🏛️ Balance General"
        ]
    )

    if subm_cont == "📖 Libro Diario":
        st.header("📖 Libro Diario Contable")
        with st.expander("➕ Registrar Nuevo Asiento Contable", expanded=True):
            f_asiento = st.date_input("Fecha", datetime.now())
            num_asiento = st.number_input("Número Asiento", value=int(st.session_state['num_asiento']))
            concepto = st.text_input("Concepto", value="Asiento de Apertura")
            
            c1, c2 = st.columns(2)
            cuenta_debe = c1.selectbox("Cuenta Cargo (DEBE)", CATALOGO_CUENTAS, index=0)
            monto_debe = c1.number_input("Monto DEBE ($)", min_value=0.0, value=1000.0)
            
            cuenta_haber = c2.selectbox("Cuenta Abono (HABER)", CATALOGO_CUENTAS, index=12)
            monto_haber = c2.number_input("Monto HABER ($)", min_value=0.0, value=1000.0)

            if st.button("💾 Guardar Asiento"):
                if monto_debe == monto_haber and monto_debe > 0:
                    st.session_state['libro_diario'].append({
                        "Asiento": num_asiento, "Fecha": f_asiento.strftime("%Y-%m-%d"),
                        "Concepto": concepto, "Cuenta Debe": cuenta_debe, "Debe": monto_debe,
                        "Cuenta Haber": cuenta_haber, "Haber": monto_haber
                    })
                    st.session_state['num_asiento'] += 1
                    st.success("✅ Asiento guardado correctamente.")
                else:
                    st.error("❌ La partida doble no cuadra.")

        if len(st.session_state['libro_diario']) > 0:
            st.dataframe(pd.DataFrame(st.session_state['libro_diario']), use_container_width=True, hide_index=True)

    elif subm_cont == "⚖️ Cuentas T (Esquemas de Mayor)":
        st.header("⚖️ Cuentas T (Esquemas de Mayor)")
        if len(st.session_state['libro_diario']) > 0:
            df_diario = pd.DataFrame(st.session_state['libro_diario'])
            cuentas_usadas = set(df_diario['Cuenta Debe']).union(set(df_diario['Cuenta Haber']))
            
            for cuenta in cuentas_usadas:
                st.subheader(f"Cuenta: {cuenta}")
                debes = df_diario[df_diario['Cuenta Debe'] == cuenta][['Asiento', 'Debe']].rename(columns={'Debe': 'Monto'})
                haberes = df_diario[df_diario['Cuenta Haber'] == cuenta][['Asiento', 'Haber']].rename(columns={'Haber': 'Monto'})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**DEBE (Cargos)**")
                    st.dataframe(debes, use_container_width=True, hide_index=True)
                    tot_debe = debes['Monto'].sum()
                    st.markdown(f"**Total Cargos:** ${tot_debe:.2f}")
                with col2:
                    st.markdown("**HABER (Abonos)**")
                    st.dataframe(haberes, use_container_width=True, hide_index=True)
                    tot_haber = haberes['Monto'].sum()
                    st.markdown(f"**Total Abonos:** ${tot_haber:.2f}")
                st.markdown("---")
        else:
            st.info("No hay asientos registrados para generar las Cuentas T.")

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
        utilidad_operacion = utilidad_bruta - (gastos_admin + gastos_venta)

        st.metric("Ventas Totales", f"${ventas:.2f}")
        st.metric("Costo de Ventas", f"${costo_ventas:.2f}")
        st.metric("Utilidad Bruta", f"${utilidad_bruta:.2f}")
        st.metric("Gastos Operativos", f"${gastos_admin + gastos_venta:.2f}")
        st.metric("Utilidad del Ejercicio", f"${utilidad_operacion:.2f}", delta=f"${utilidad_operacion:.2f}")

    elif subm_cont == "🏛️ Balance General":
        st.header("🏛️ Balance General (Estado de Situación Financiera)")
        
        # Cálculo de saldos desde el Libro Diario
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
            st.write(f"**Circulante:** ${tot_circulante:.2f}")
            st.write(f"**No Circulante:** ${tot_no_circulante:.2f}")
            st.markdown(f"### **TOTAL ACTIVO:** ${tot_activo:.2f}")

        with col2:
            st.subheader("PASIVO Y CAPITAL")
            st.write(f"**Pasivo Corto Plazo:** ${tot_pasivo:.2f}")
            st.write(f"**Capital Social:** ${capital_social:.2f}")
            st.markdown(f"### **TOTAL PASIVO + CAPITAL:** ${tot_pasivo_capital:.2f}")

        st.markdown("---")
        if tot_activo == tot_pasivo_capital:
            st.success("⚖️ ¡El Balance General está perfectamente cuadrado!")
        else:
            st.warning("⚠️ El Balance General presenta una diferencia en la ecuación contable.")
