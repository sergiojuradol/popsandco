import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="POPS & CO - Sistema Integral",
    page_icon="🍿",
    layout="wide"
)

# ---------------------------------------------------------
# CATALOGO OFICIAL DE CUENTAS CONTABLES (PDF POPS & CO)
# ---------------------------------------------------------
CATALOGO_CUENTAS = [
    # Activo Circulante
    "Bancos",
    "Caja",
    "Clientes",
    "Almacén de materia prima",
    "Almacén de material indirecto",
    "Almacén de producto terminado",
    "Deudores diversos",
    # Activo No Circulante
    "Mobiliario",
    "Maquinaria y Equipo de Fabricación",
    # Pasivo Corto Plazo
    "Proveedores",
    "Acreedores Bancarios",
    "Acreedores Diversos",
    # Capital Contable
    "Capital Social",
    "Utilidad del ejercicio",
    # Transitorias
    "Nómina Operativa",
    # Cuentas de Estado (Ingresos, Egresos, Gastos)
    "Ventas",
    "Otros productos",
    "Costo de ventas",
    "Gastos de administración",
    "Gastos de venta",
    "Gastos financieros",
    "Honorarios a socios"
]

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

if 'historial_mermas' not in st.session_state:
    st.session_state['historial_mermas'] = []

if 'historial_ventas' not in st.session_state:
    st.session_state['historial_ventas'] = []

if 'historial_lotes' not in st.session_state:
    st.session_state['historial_lotes'] = []

# ESTADO DE LIBRO DIARIO CONTABLE
if 'libro_diario' not in st.session_state:
    st.session_state['libro_diario'] = []

if 'num_asiento' not in st.session_state:
    st.session_state['num_asiento'] = 1


# ---------------------------------------------------------
# MENÚ LATERAL Y NAVEGACIÓN PRINCIPAL
# ---------------------------------------------------------
st.sidebar.title("🍿 POPS & CO")
modulo_principal = st.sidebar.selectbox(
    "Selecciona Módulo:",
    ["🏠 Inicio", "⚙️ MÓDULO 1: OPERATIVO / PRODUCCIÓN", "📊 MÓDULO 2: CONTABILIDAD"]
)

# ---------------------------------------------------------
# MÓDULO 0: INICIO / INTERFAZ PRINCIPAL
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

    st.subheader("🚀 ¿Qué deseas hacer hoy?")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.info("### ⚙️ Operativo y Producción\nControl de existencias de materia prima, empaques, lotes de fabricación y ventas físicas.")
    
    with col_b:
        st.success("### 📖 Libro Diario\nRegistro de asientos contables con partida doble y llenado automático de Cuentas T.")

    with col_c:
        st.warning("### 📈 Estado de Resultados\nConsulta financiera automática mensual con utilidades e ingresos consolidados.")

# ---------------------------------------------------------
# MÓDULO 1: OPERATIVO O MÓDULO DE PRODUCCIÓN
# ---------------------------------------------------------
elif modulo_principal == "⚙️ MÓDULO 1: OPERATIVO / PRODUCCIÓN":
    st.sidebar.markdown("---")
    subm_op = st.sidebar.radio(
        "Secciones Operativas:",
        [
            "📦 Inventario de Producto Terminado",
            "🌾 Materia Prima (Físico y Movimientos)",
            "🛒 Compras e Ingreso de Insumos",
            "🏭 Registrar Lote de Producción y Costos",
            "🛍️ Punto de Venta y Margen de Ganancia",
            "💰 Costos Promedio, BOM y Valuación",
            "⚠️ Control de Mermas y Diferencias"
        ]
    )

    if subm_op == "📦 Inventario de Producto Terminado":
        st.header("📦 Inventario de Producto Terminado (Almacén de Salida)")
        st.caption("Consulta del stock disponible para venta y ajuste directo por mermas o roturas.")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📊 Stock Actual de Paquetes")
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
            st.subheader("✏️ Ajuste / Mermas de Producto Terminado")
            prod_ajuste = st.selectbox("Selecciona Producto", list(st.session_state['inventario_pt'].keys()))
            cant_actual = st.session_state['inventario_pt'][prod_ajuste]['cant']
            
            tipo_ajuste = st.radio("Acción", ["Restar / Tirar (Merma)", "Sumar (Ajuste Manual)"], horizontal=True)
            cant_cambio = st.number_input("Cantidad de Paquetes", min_value=1, value=1)
            motivo = st.text_input("Motivo del ajuste", value="Empaque dañado / Bolsa abierta")

            if st.button("Aplicar Ajuste a Producto Terminado"):
                if "Restar" in tipo_ajuste:
                    if cant_actual >= cant_cambio:
                        st.session_state['inventario_pt'][prod_ajuste]['cant'] -= cant_cambio
                        st.session_state['historial_mermas'].append({
                            "Concepto": f"Merma de Producto Terminado ({prod_ajuste})",
                            "Cantidad": f"{cant_cambio} pkts",
                            "Detalle": motivo
                        })
                        st.warning(f"⚠️ Se descontaron {cant_cambio} paquetes de {prod_ajuste}. Stock actual: {st.session_state['inventario_pt'][prod_ajuste]['cant']}")
                    else:
                        st.error("No puedes restar más paquetes de los que existen en stock.")
                else:
                    st.session_state['inventario_pt'][prod_ajuste]['cant'] += cant_cambio
                    st.success(f"✅ Se agregaron {cant_cambio} paquetes a {prod_ajuste}. Stock actual: {st.session_state['inventario_pt'][prod_ajuste]['cant']}")

    elif subm_op == "🌾 Materia Prima (Físico y Movimientos)":
        st.header("🌾 Materias Primas e Empaques (Existencias Físicas)")
        tab1, tab2 = st.tabs(["📋 Stock Físico de Insumos", "📜 Historial de Movimientos (Kárdex)"])

        with tab1:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Materia Prima Directa")
                filas_mp = []
                for k, v in st.session_state['inventario_mp'].items():
                    if "cant_kg" in v:
                        filas_mp.append({"Insumo": k, "Cantidad Disponible": f"{v['cant_kg']:.2f} kg"})
                    elif "cant_l" in v:
                        filas_mp.append({"Insumo": k, "Cantidad Disponible": f"{v['cant_l']:.2f} L"})
                    else:
                        filas_mp.append({"Insumo": k, "Cantidad Disponible": f"{v['cant_g']:.0f} g"})
                st.dataframe(pd.DataFrame(filas_mp), use_container_width=True, hide_index=True)

            with col_b:
                st.subheader("Empaques e Indirectos")
                filas_ind = []
                for k, v in st.session_state['inventario_indirectos'].items():
                    filas_ind.append({"Material": k, "Piezas Disponibles": f"{v['cant']} pzs"})
                st.dataframe(pd.DataFrame(filas_ind), use_container_width=True, hide_index=True)

        with tab2:
            st.subheader("📜 Bitácora de Entradas y Salidas (Kárdex)")
            if len(st.session_state['historial_movimientos_mp']) > 0:
                df_mov = pd.DataFrame(st.session_state['historial_movimientos_mp'])
                st.dataframe(df_mov.iloc[::-1], use_container_width=True, hide_index=True)
            else:
                st.info("No hay movimientos registrados.")

    elif subm_op == "🛒 Compras e Ingreso de Insumos":
        st.header("🛒 Registrar Compra de Materia Prima / Empaques")
        cat_compra = st.radio("Categoría de Compra", ["Materia Prima Directa", "Empaques / Etiquetas"], horizontal=True)
        f_act = datetime.now().strftime("%Y-%m-%d %H:%M")

        if cat_compra == "Materia Prima Directa":
            insumo_sel = st.selectbox("Selecciona Insumo Comprado", list(st.session_state['inventario_mp'].keys()))

            if insumo_sel == "Maíz":
                col1, col2 = st.columns(2)
                kg_comprados = col1.number_input("Kilos de Maíz Comprados", min_value=1.0, value=20.0, step=1.0)
                precio_total = col2.number_input("Precio Total Pagado ($)", min_value=0.0, value=360.0)

                if st.button("➕ Registrar Compra de Maíz"):
                    curr_kg = st.session_state['inventario_mp']['Maíz']['cant_kg']
                    curr_costo = st.session_state['inventario_mp']['Maíz']['costo_promedio_kg']
                    nuevo_total_kg = curr_kg + kg_comprados
                    nuevo_costo_prom = ((curr_kg * curr_costo) + precio_total) / nuevo_total_kg

                    st.session_state['inventario_mp']['Maíz']['cant_kg'] = nuevo_total_kg
                    st.session_state['inventario_mp']['Maíz']['costo_promedio_kg'] = nuevo_costo_prom

                    st.session_state['historial_movimientos_mp'].append({
                        "Fecha": f_act, "Insumo": "Maíz", "Tipo": "Entrada por Compra",
                        "Cantidad": f"+{kg_comprados:.2f} kg", "Detalle": f"Compra por ${precio_total:.2f}"
                    })
                    st.success(f"✅ Compra registrada! Maíz en stock: {nuevo_total_kg:.2f} kg | Nuevo Costo Promedio: ${nuevo_costo_prom:.2f}/kg")

            elif insumo_sel == "Aceite":
                col1, col2 = st.columns(2)
                litros_comprados = col1.number_input("Litros de Aceite Comprados", min_value=0.5, value=10.0, step=0.5)
                precio_total = col2.number_input("Precio Total Pagado ($)", min_value=0.0, value=375.0)

                if st.button("➕ Registrar Compra de Aceite"):
                    curr_l = st.session_state['inventario_mp']['Aceite']['cant_l']
                    curr_costo = st.session_state['inventario_mp']['Aceite']['costo_promedio_l']
                    nuevo_total_l = curr_l + litros_comprados
                    nuevo_costo_prom = ((curr_l * curr_costo) + precio_total) / nuevo_total_l

                    st.session_state['inventario_mp']['Aceite']['cant_l'] = nuevo_total_l
                    st.session_state['inventario_mp']['Aceite']['costo_promedio_l'] = nuevo_costo_prom

                    st.session_state['historial_movimientos_mp'].append({
                        "Fecha": f_act, "Insumo": "Aceite", "Tipo": "Entrada por Compra",
                        "Cantidad": f"+{litros_comprados:.2f} L", "Detalle": f"Compra por ${precio_total:.2f}"
                    })
                    st.success(f"✅ Compra registrada! Aceite en stock: {nuevo_total_l:.2f} L | Nuevo Costo Promedio: ${nuevo_costo_prom:.2f}/L")

            else:
                col1, col2 = st.columns(2)
                kilos_comprados = col1.number_input(f"Kilos de {insumo_sel} Comprados", min_value=0.1, value=1.0, step=0.1)
                precio_total = col2.number_input("Precio Total Pagado ($)", min_value=0.0, value=160.0)

                if st.button(f"➕ Registrar Compra de {insumo_sel}"):
                    gramos_nuevos = kilos_comprados * 1000.0
                    curr_g = st.session_state['inventario_mp'][insumo_sel]['cant_g']
                    curr_costo_kg = st.session_state['inventario_mp'][insumo_sel]['costo_promedio_kg']
                    nuevo_total_g = curr_g + gramos_nuevos
                    nuevo_costo_prom_kg = (((curr_g / 1000.0) * curr_costo_kg) + precio_total) / (nuevo_total_g / 1000.0)

                    st.session_state['inventario_mp'][insumo_sel]['cant_g'] = nuevo_total_g
                    st.session_state['inventario_mp'][insumo_sel]['costo_promedio_kg'] = nuevo_costo_prom_kg

                    st.session_state['historial_movimientos_mp'].append({
                        "Fecha": f_act, "Insumo": insumo_sel, "Tipo": "Entrada por Compra",
                        "Cantidad": f"+{gramos_nuevos:.0f} g", "Detalle": f"Compra por ${precio_total:.2f}"
                    })
                    st.success(f"✅ Compra registrada! {insumo_sel} en stock: {nuevo_total_g:.0f} g | Nuevo Costo Promedio: ${nuevo_costo_prom_kg:.2f}/kg")

        else:
            mat_sel = st.selectbox("Selecciona Material Indirecto", list(st.session_state['inventario_indirectos'].keys()))
            col1, col2 = st.columns(2)
            pzs_compradas = col1.number_input("Piezas Compradas", min_value=1, value=2000 if "Bolsas" in mat_sel else 500)
            precio_total = col2.number_input("Precio Total Pagado ($)", min_value=0.0, value=800.0 if "Bolsas" in mat_sel else 875.0)

            if st.button(f"➕ Registrar Compra de {mat_sel}"):
                curr_pzs = st.session_state['inventario_indirectos'][mat_sel]['cant']
                curr_costo_u = st.session_state['inventario_indirectos'][mat_sel]['costo_u']
                nuevo_total_pzs = curr_pzs + pzs_compradas
                nuevo_costo_u = ((curr_pzs * curr_costo_u) + precio_total) / nuevo_total_pzs

                st.session_state['inventario_indirectos'][mat_sel]['cant'] = nuevo_total_pzs
                st.session_state['inventario_indirectos'][mat_sel]['costo_u'] = nuevo_costo_u

                st.session_state['historial_movimientos_mp'].append({
                    "Fecha": f_act, "Insumo": mat_sel, "Tipo": "Entrada por Compra",
                    "Cantidad": f"+{pzs_compradas} pzs", "Detalle": f"Compra de empaques por ${precio_total:.2f}"
                })
                st.success(f"✅ Compra registrada! {mat_sel} en stock: {nuevo_total_pzs} pzs | Nuevo Costo Unitario: ${nuevo_costo_u:.2f}")

    elif subm_op == "🏭 Registrar Lote de Producción y Costos":
        st.header("⚙️ Registro de Lote de Producción y Costos Directos")
        
        st.subheader("1. Producción Planeada por Sabor (Paquetes Listos)")
        c1, c2, c3, c4, c5 = st.columns(5)
        up_trad = c1.number_input("Tradicional (120g)", min_value=0, value=40)
        up_ched = c2.number_input("Cheddar (120g)", min_value=0, value=65)
        up_qjal = c3.number_input("Queso Jalapeño (120g)", min_value=0, value=25)
        up_hab = c4.number_input("Habanero (120g)", min_value=0, value=45)
        up_ado = c5.number_input("Adobado (120g)", min_value=0, value=35)

        up_65g = st.number_input("Paquetes de Pedido Especial (65g - Opcional)", min_value=0, value=0)

        total_pkts_120 = up_trad + up_ched + up_qjal + up_hab + up_ado
        total_pkts_general = total_pkts_120 + up_65g

        maiz_teorico_kg = ((total_pkts_120 * 120.0) + (up_65g * 65.0)) / 1000.0
        aceite_teorico_l = total_pkts_general / 39.0

        st.markdown("---")
        st.subheader("2. Consumo Real de Insumos")
        col_a, col_b = st.columns(2)

        with col_a:
            maiz_real = st.number_input("Maíz Consumido Real (kg)", min_value=0.0, value=float(maiz_teorico_kg))
            aceite_real = st.number_input("Aceite Consumido Real (L)", min_value=0.0, value=float(aceite_teorico_l))
            bolsas_reales = st.number_input("Bolsas Celofán Utilizadas (pzs)", min_value=0, value=total_pkts_general + 5)

        with col_b:
            flavacol_real_g = st.number_input("Flavacol Usado (g)", min_value=0.0, value=up_trad * 11.76)
            saz_ched_real = st.number_input("Sazonador Cheddar Usado (g)", min_value=0.0, value=up_ched * (1000.0 / 85.0))
            saz_qjal_real = st.number_input("Sazonador Q. Jalapeño Usado (g)", min_value=0.0, value=up_qjal * (1000.0 / 85.0))
            saz_hab_real = st.number_input("Sazonador Habanero Usado (g)", min_value=0.0, value=up_hab * (1000.0 / 85.0))
            saz_ado_real = st.number_input("Sazonador Adobo Usado (g)", min_value=0.0, value=up_ado * (1000.0 / 85.0))

        st.markdown("---")
        st.subheader("3. Mano de Obra Directa (MOD) y Servicios (Gas) para este Lote")
        col_mod1, col_mod2, col_gas = st.columns(3)

        horas_mod = col_mod1.number_input("Horas de Trabajo Invertidas", min_value=0.0, value=3.0, step=0.5)
        costo_hora_mod = col_mod2.number_input("Costo por Hora de Mano de Obra ($)", min_value=0.0, value=60.0, step=5.0)
        costo_gas_lote = col_gas.number_input("Costo Estimado de Gas/Energía ($)", min_value=0.0, value=85.0, step=5.0)

        costo_total_mod = horas_mod * costo_hora_mod

        costo_maiz_dinero = maiz_real * st.session_state['inventario_mp']['Maíz']['costo_promedio_kg']
        costo_aceite_dinero = aceite_real * st.session_state['inventario_mp']['Aceite']['costo_promedio_l']
        costo_flava_dinero = (flavacol_real_g / 1000.0) * st.session_state['inventario_mp']['Flavacol']['costo_promedio_kg']
        costo_ched_dinero = (saz_ched_real / 1000.0) * st.session_state['inventario_mp']['Sazonador Cheddar']['costo_promedio_kg']
        costo_qjal_dinero = (saz_qjal_real / 1000.0) * st.session_state['inventario_mp']['Sazonador Queso Jalapeño']['costo_promedio_kg']
        costo_hab_dinero = (saz_hab_real / 1000.0) * st.session_state['inventario_mp']['Sazonador Habanero']['costo_promedio_kg']
        costo_ado_dinero = (saz_ado_real / 1000.0) * st.session_state['inventario_mp']['Sazonador Adobo']['costo_promedio_kg']

        tot_mp_dinero = costo_maiz_dinero + costo_aceite_dinero + costo_flava_dinero + costo_ched_dinero + costo_qjal_dinero + costo_hab_dinero + costo_ado_dinero

        costo_bolsas_dinero = bolsas_reales * st.session_state['inventario_indirectos']['Bolsas Celofán 20x35 (pzs)']['costo_u']
        costo_etiq_dinero = (
            (up_trad * st.session_state['inventario_indirectos']['Etiquetas 120g Tradicional (pzs)']['costo_u']) +
            (up_ched * st.session_state['inventario_indirectos']['Etiquetas 120g Cheddar (pzs)']['costo_u']) +
            (up_qjal * st.session_state['inventario_indirectos']['Etiquetas 120g Queso Jalapeño (pzs)']['costo_u']) +
            (up_hab * st.session_state['inventario_indirectos']['Etiquetas 120g Habanero (pzs)']['costo_u']) +
            (up_ado * st.session_state['inventario_indirectos']['Etiquetas 120g Adobo (pzs)']['costo_u']) +
            (up_65g * st.session_state['inventario_indirectos']['Etiquetas 65g (pzs)']['costo_u'])
        )

        tot_empaques_dinero = costo_bolsas_dinero + costo_etiq_dinero
        costo_total_lote_dinero = tot_mp_dinero + tot_empaques_dinero + costo_total_mod + costo_gas_lote
        costo_promedio_por_bolsa = (costo_total_lote_dinero / total_pkts_general) if total_pkts_general > 0 else 0.0

        st.markdown("---")
        st.subheader("💰 Resumen Previo de Costos del Lote")

        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        col_res1.metric("Materia Prima Directa", f"${tot_mp_dinero:.2f}")
        col_res2.metric("Empaques y Etiquetas", f"${tot_empaques_dinero:.2f}")
        col_res3.metric("Mano de Obra y Gas", f"${costo_total_mod + costo_gas_lote:.2f}")
        col_res4.metric("Costo Total en Dinero", f"${costo_total_lote_dinero:.2f}")

        if st.button("🚀 Procesar Lote: Descontar Inventarios y Registrar Costos"):
            if total_pkts_general > 0:
                f_act = datetime.now().strftime("%Y-%m-%d %H:%M")

                st.session_state['inventario_mp']["Maíz"]["cant_kg"] -= maiz_real
                st.session_state['inventario_mp']["Aceite"]["cant_l"] -= aceite_real
                if flavacol_real_g > 0: st.session_state['inventario_mp']["Flavacol"]["cant_g"] -= flavacol_real_g
                if saz_ched_real > 0: st.session_state['inventario_mp']["Sazonador Cheddar"]["cant_g"] -= saz_ched_real
                if saz_qjal_real > 0: st.session_state['inventario_mp']["Sazonador Queso Jalapeño"]["cant_g"] -= saz_qjal_real
                if saz_hab_real > 0: st.session_state['inventario_mp']["Sazonador Habanero"]["cant_g"] -= saz_hab_real
                if saz_ado_real > 0: st.session_state['inventario_mp']["Sazonador Adobo"]["cant_g"] -= saz_ado_real

                st.session_state['inventario_indirectos']["Bolsas Celofán 20x35 (pzs)"]["cant"] -= bolsas_reales
                if up_trad > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Tradicional (pzs)"]["cant"] -= up_trad
                if up_ched > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Cheddar (pzs)"]["cant"] -= up_ched
                if up_qjal > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Queso Jalapeño (pzs)"]["cant"] -= up_qjal
                if up_hab > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Habanero (pzs)"]["cant"] -= up_hab
                if up_ado > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Adobo (pzs)"]["cant"] -= up_ado
                if up_65g > 0: st.session_state['inventario_indirectos']["Etiquetas 65g (pzs)"]["cant"] -= up_65g

                st.session_state['inventario_pt']["Tradicional (120g)"]["cant"] += up_trad
                st.session_state['inventario_pt']["Cheddar (120g)"]["cant"] += up_ched
                st.session_state['inventario_pt']["Queso Jalapeño (120g)"]["cant"] += up_qjal
                st.session_state['inventario_pt']["Habanero (120g)"]["cant"] += up_hab
                st.session_state['inventario_pt']["Adobado (120g)"]["cant"] += up_ado
                st.session_state['inventario_pt']["Pedido Especial (65g)"]["cant"] += up_65g

                st.session_state['historial_lotes'].append({
                    "Fecha": f_act,
                    "Paquetes Producidos": total_pkts_general,
                    "Costo MP": f"${tot_mp_dinero:.2f}",
                    "Costo Empaques": f"${tot_empaques_dinero:.2f}",
                    "Mano de Obra": f"${costo_total_mod:.2f}",
                    "Gas/Servicios": f"${costo_gas_lote:.2f}",
                    "Costo Total Lote": f"${costo_total_lote_dinero:.2f}",
                    "Costo Promedio/Bolsa": f"${costo_promedio_por_bolsa:.2f}"
                })

                st.balloons()
                st.success(f"✅ ¡Lote procesado! Costo total: ${costo_total_lote_dinero:.2f} | Costo/paquete: ${costo_promedio_por_bolsa:.2f}")

    elif subm_op == "🛍️ Punto de Venta y Margen de Ganancia":
        st.header("🛍️ Registro de Ventas a Distribuidores y Margen Bruto")
        sabor_venta = st.selectbox("Selecciona Producto / Sabor", list(st.session_state['inventario_pt'].keys()))
        stock_disp = st.session_state['inventario_pt'][sabor_venta]['cant']
        precio_u = st.session_state['inventario_pt'][sabor_venta]['precio_dist']
        costo_dir_u = st.session_state['inventario_pt'][sabor_venta].get('costo_directo_u', 5.50)

        col_v1, col_v2 = st.columns(2)
        cant_vender = col_v1.number_input("Cantidad a Vender (pkts)", min_value=1, max_value=max(1, stock_disp), value=min(10, max(1, stock_disp)))
        cliente = col_v2.text_input("Nombre de Distribuidor / Cliente", value="Distribuidor General")

        total_cobrar = cant_vender * precio_u
        total_costo_venta = cant_vender * costo_dir_u
        ganancia_bruta_total = total_cobrar - total_costo_venta

        st.markdown(f"### Total Venta: **${total_cobrar:.2f}** | Ganancia Bruta Real: **${ganancia_bruta_total:.2f}**")

        if st.button("💵 Confirmar y Registrar Venta"):
            if stock_disp >= cant_vender:
                st.session_state['inventario_pt'][sabor_venta]['cant'] -= cant_vender
                st.session_state['historial_ventas'].append({
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Cliente": cliente,
                    "Producto": sabor_venta,
                    "Cantidad": cant_vender,
                    "Total Cobrado": f"${total_cobrar:.2f}",
                    "Costo de Venta": f"${total_costo_venta:.2f}",
                    "Ganancia Bruta": f"${ganancia_bruta_total:.2f}"
                })
                st.success(f"✅ Venta registrada! Se descontaron {cant_vender} pkts.")

    elif subm_op == "💰 Costos Promedio, BOM y Valuación":
        st.header("💰 Módulo Financiero: Costos Promedio y BOM por Receta")
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            st.subheader("🌾 Costos Promedio - Materia Prima Directa")
            filas_c_mp = []
            for k, v in st.session_state['inventario_mp'].items():
                if "cant_kg" in v:
                    filas_c_mp.append({"Insumo": k, "Stock": f"{v['cant_kg']:.2f} kg", "Costo Promedio": f"${v['costo_promedio_kg']:.2f} / kg"})
                elif "cant_l" in v:
                    filas_c_mp.append({"Insumo": k, "Stock": f"{v['cant_l']:.2f} L", "Costo Promedio": f"${v['costo_promedio_l']:.2f} / L"})
                else:
                    filas_c_mp.append({"Insumo": k, "Stock": f"{v['cant_g']:.0f} g", "Costo Promedio": f"${v['costo_promedio_kg']:.2f} / kg"})
            st.dataframe(pd.DataFrame(filas_c_mp), use_container_width=True, hide_index=True)

        with col_c2:
            st.subheader("📦 Costos Unitarios - Empaques e Indirectos")
            filas_c_ind = []
            for k, v in st.session_state['inventario_indirectos'].items():
                filas_c_ind.append({"Material": k, "Stock": f"{v['cant']} pzs", "Costo Unitario": f"${v['costo_u']:.2f} / pza"})
            st.dataframe(pd.DataFrame(filas_c_ind), use_container_width=True, hide_index=True)

    elif subm_op == "⚠️ Control de Mermas y Diferencias":
        st.header("📋 Historial de Mermas y Desperdicios")
        if len(st.session_state['historial_mermas']) > 0:
            st.dataframe(pd.DataFrame(st.session_state['historial_mermas']), use_container_width=True, hide_index=True)
        else:
            st.info("👌 No hay mermas registradas por el momento.")

# ---------------------------------------------------------
# MÓDULO 2: CONTABILIDAD COMPLETA (PDF POPS & CO)
# ---------------------------------------------------------
elif modulo_principal == "📊 MÓDULO 2: CONTABILIDAD":
    st.sidebar.markdown("---")
    subm_cont = st.sidebar.radio(
        "Secciones Contables:",
        [
            "📖 Libro Diario",
            "⚖️ Cuentas T (Esquemas de Mayor)",
            "📈 Estado de Resultados (Mensual)"
        ]
    )

    # -----------------------------------------------------
    # LIBRO DIARIO
    # -----------------------------------------------------
    if subm_cont == "📖 Libro Diario":
        st.header("📖 Libro Diario Contable")
        st.caption("Registra tus asientos contables con partida doble exactos. Las Cuentas T y el Estado de Resultados se llenarán solos.")

        with st.expander("➕ Registrar Nuevo Asiento Contable", expanded=True):
            f_asiento = st.date_input("Fecha del Asiento", datetime.now())
            num_asiento_actual = st.number_input("Número de Asiento", value=int(st.session_state['num_asiento']), step=1)
            concepto_general = st.text_input("Concepto / Descripción del Asiento", value="Compra de materia prima / Venta del día")

            st.markdown("---")
            st.subheader("Movimientos del Asiento (Partida Doble)")

            col_c1, col_c2, col_c3, col_c4 = st.columns([3, 2, 2, 2])
            
            with col_c1:
                cuenta_debe = st.selectbox("Cuenta del DEBE (Cargo)", CATALOGO_CUENTAS, index=0)
            with col_c2:
                parcial_debe = st.number_input("Parcial Debe ($)", min_value=0.0, value=0.0)
            with col_c3:
                monto_debe = st.number_input("Monto DEBE ($)", min_value=0.0, value=100.0)

            col_h1, col_h2, col_h3, col_h4 = st.columns([3, 2, 2, 2])
            
            with col_h1:
                cuenta_haber = st.selectbox("Cuenta del HABER (Abono)", CATALOGO_CUENTAS, index=1)
            with col_h2:
                parcial_haber = st.number_input("Parcial Haber ($)", min_value=0.0, value=0.0)
            with col_h3:
                monto_haber = st.number_input("Monto HABER ($)", min_value=0.0, value=100.0)

            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("💾 Guardar Asiento en Libro Diario"):
                if monto_debe != monto_haber:
                    st.error(f"❌ La partida doble no cuadra. DEBE (${monto_debe:.2f}) debe ser igual al HABER (${monto_haber:.2f}).")
                elif monto_debe <= 0:
                    st.error("❌ El monto debe ser mayor a 0.")
                else:
                    f_str = f_asiento.strftime("%Y-%m-%d")
                    
                    # Movimiento DEBE
                    st.session_state['libro_diario'].append({
                        "Fecha": f_str,
                        "No. Asiento": num_asiento_actual,
                        "Concepto": concepto_general,
                        "Cuenta": cuenta_debe,
                        "Parcial": f"${parcial_debe:.2f}" if parcial_debe > 0 else "-",
                        "Debe": monto_debe,
                        "Haber": 0.0
                    })
                    
                    # Movimiento HABER
                    st.session_state['libro_diario'].append({
                        "Fecha": f_str,
                        "No. Asiento": num_asiento_actual,
                        "Concepto": concepto_general,
                        "Cuenta": cuenta_haber,
                        "Parcial": f"${parcial_haber:.2f}" if parcial_haber > 0 else "-",
                        "Debe": 0.0,
                        "Haber": monto_haber
                    })

                    st.session_state['num_asiento'] = num_asiento_actual + 1
                    st.success(f"✅ Asiento No. {num_asiento_actual} registrado correctamente.")

        st.markdown("---")
        st.subheader("📜 Registros del Libro Diario")
        if len(st.session_state['libro_diario']) > 0:
            df_diario = pd.DataFrame(st.session_state['libro_diario'])
            df_mostrar = df_diario.copy()
            df_mostrar["Debe"] = df_mostrar["Debe"].apply(lambda x: f"${x:.2f}" if x > 0 else "-")
            df_mostrar["Haber"] = df_mostrar["Haber"].apply(lambda x: f"${x:.2f}" if x > 0 else "-")
            
            st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

            tot_debe = df_diario["Debe"].sum()
            tot_haber = df_diario["Haber"].sum()
            
            st.info(f"⚖️ **Sumas Iguales Contables:** DEBE: **${tot_debe:.2f}** | HABER: **${tot_haber:.2f}**")
        else:
            st.info("Aún no se han registrado asientos en el Libro Diario.")

    # -----------------------------------------------------
    # CUENTAS T
    # -----------------------------------------------------
    elif subm_cont == "⚖️ Cuentas T (Esquemas de Mayor)":
        st.header("⚖️ Cuentas T / Esquemas de Mayor")
        st.caption("Generación automática a partir de los asientos registrados en el Libro Diario.")

        if len(st.session_state['libro_diario']) == 0:
            st.info("Llena asientos en el Libro Diario para ver tus Cuentas T automáticamente.")
        else:
            df_d = pd.DataFrame(st.session_state['libro_diario'])
            cuentas_usadas = df_d["Cuenta"].unique()

            cols = st.columns(2)
            idx = 0

            for c in CATALOGO_CUENTAS:
                if c in cuentas_usadas:
                    df_c = df_d[df_d["Cuenta"] == c]
                    total_debe = df_c["Debe"].sum()
                    total_haber = df_c["Haber"].sum()
                    saldo = total_debe - total_haber

                    with cols[idx % 2]:
                        st.markdown(f"### **{c}**")
                        
                        df_t = df_c[["No. Asiento", "Debe", "Haber"]].copy()
                        df_t["Debe"] = df_t["Debe"].apply(lambda x: f"${x:.2f}" if x > 0 else "")
                        df_t["Haber"] = df_t["Haber"].apply(lambda x: f"${x:.2f}" if x > 0 else "")

                        st.table(df_t)
                        st.markdown(f"**Suma Debe:** ${total_debe:.2f} | **Suma Haber:** ${total_haber:.2f}")
                        
                        if saldo >= 0:
                            st.success(f"**Saldo Deudor:** ${saldo:.2f}")
                        else:
                            st.warning(f"**Saldo Acreedor:** ${abs(saldo):.2f}")
                        
                        st.markdown("---")
                    idx += 1

    # -----------------------------------------------------
    # ESTADO DE RESULTADOS
    # -----------------------------------------------------
    elif subm_cont == "📈 Estado de Resultados (Mensual)":
        st.header("📈 Estado de Resultados Consolidado")
        st.caption("Cálculo automático de ingresos, costos y gastos acumulados.")

        if len(st.session_state['libro_diario']) == 0:
            st.info("No hay datos en el Libro Diario para generar el Estado de Resultados.")
        else:
            df_d = pd.DataFrame(st.session_state['libro_diario'])

            # Función para obtener saldo neto de una cuenta de estado
            def get_saldo(cuenta_nombre):
                df_c = df_d[df_d["Cuenta"] == cuenta_nombre]
                if len(df_c) == 0:
                    return 0.0
                return df_c["Haber"].sum() - df_c["Debe"].sum()

            def get_saldo_egreso(cuenta_nombre):
                df_c = df_d[df_d["Cuenta"] == cuenta_nombre]
                if len(df_c) == 0:
                    return 0.0
                return df_c["Debe"].sum() - df_c["Haber"].sum()

            ventas = get_saldo("Ventas")
            otros_prod = get_saldo("Otros productos")
            ingresos_totales = ventas + otros_prod

            costo_ventas = get_saldo_egreso("Costo de ventas")
            utilidad_bruta = ingresos_totales - costo_ventas

            g_admin = get_saldo_egreso("Gastos de administración")
            g_venta = get_saldo_egreso("Gastos de venta")
            g_fin = get_saldo_egreso("Gastos financieros")
            honorarios = get_saldo_egreso("Honorarios a socios")

            gastos_operativos_totales = g_admin + g_venta + g_fin + honorarios
            utilidad_neta = utilidad_bruta - gastos_operativos_totales

            st.markdown("### 📊 POPS & CO - Estado de Resultados")
            st.markdown(f"**Ventas Totales:** ${ventas:.2f}")
            st.markdown(f"**Otros Productos:** ${otros_prod:.2f}")
            st.markdown(f"**(=) Ingresos Totales:** **${ingresos_totales:.2f}**")
            st.markdown("---")
            st.markdown(f"**(-) Costo de Ventas:** ${costo_ventas:.2f}")
            st.markdown(f"**(=) Utilidad Bruta:** **${utilidad_bruta:.2f}**")
            st.markdown("---")
            st.markdown(f"**(-) Gastos de Administración:** ${g_admin:.2f}")
            st.markdown(f"**(-) Gastos de Venta:** ${g_venta:.2f}")
            st.markdown(f"**(-) Gastos Financieros:** ${g_fin:.2f}")
            st.markdown(f"**(-) Honorarios a Socios:** ${honorarios:.2f}")
            st.markdown(f"**(=) Gastos Operativos Totales:** ${gastos_operativos_totales:.2f}")
            st.markdown("---")

            if utilidad_neta >= 0:
                st.success(f"### 🎉 Utilidad del Ejercicio: **${utilidad_neta:.2f}**")
            else:
                st.error(f"### ⚠️ Pérdida del Ejercicio: **${utilidad_neta:.2f}**")
