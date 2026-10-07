import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="POPS & CO - Control Operativo y Financiero",
    page_icon="🍿",
    layout="wide"
)

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


# ---------------------------------------------------------
# MENÚ LATERAL Y NAVEGACIÓN
# ---------------------------------------------------------
st.sidebar.title("🍿 POPS & CO")
modulo = st.sidebar.radio(
    "Menú de Navegación:",
    [
        "🏠 Inicio / Bienvenido",
        "📦 Inventario de Producto Terminado",
        "🌾 Materia Prima (Físico y Movimientos)",
        "🛒 Compras e Ingreso de Insumos",
        "🏭 Registrar Lote de Producción y Costos",
        "🛍️ Punto de Venta y Margen de Ganancia",
        "💰 Costos Promedio, BOM y Valuación",
        "⚠️ Control de Mermas y Diferencias"
    ]
)

# ---------------------------------------------------------
# MÓDULO 0: INICIO / INTERFAZ PRINCIPAL
# ---------------------------------------------------------
if modulo == "🏠 Inicio / Bienvenido":
    
    # Encabezado con Logo y Eslogan
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        # Intentar cargar la imagen del logo si existe localmente o mostrar diseño visual
        try:
            st.image("POPS & CO.png", use_column_width=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #E63946;'>🍿 POPS & CO 🍿</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #555555; font-style: italic;'>« De puñito en puñito sabe mejor »</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Tarjetas Informativas / Resumen Operativo Rápido
    st.subheader("📊 Estado General del Sistema")
    
    tot_pkts = sum(v['cant'] for v in st.session_state['inventario_pt'].values())
    tot_maiz = st.session_state['inventario_mp']['Maíz']['cant_kg']
    tot_lotes = len(st.session_state['historial_lotes'])
    tot_ventas = len(st.session_state['historial_ventas'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Producto Terminado", f"{tot_pkts} pkts")
    col2.metric("🌾 Maíz Disponible", f"{tot_maiz:.1f} kg")
    col3.metric("🏭 Lotes Procesados", f"{tot_lotes}")
    col4.metric("🛍️ Ventas Registradas", f"{tot_ventas}")

    st.markdown("---")

    # Atajos de Acceso Rápido
    st.subheader("🚀 ¿Qué deseas hacer hoy?")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.info("### 🏭 Fabricación\nRegistra un nuevo lote de producción, calcula el consumo real de maíz, empaques, mano de obra y gas.")
    
    with col_b:
        st.success("### 🛍️ Ventas\nRegistra salidas de mercancía a distribuidores y consulta el margen bruto por paquete.")

    with col_c:
        st.warning("### 🛒 Insumos\nIngresa compras de materia prima o empaques y actualiza automáticamente los costos promedio.")

# ---------------------------------------------------------
# MÓDULO 1: INVENTARIO DE PRODUCTO TERMINADO
# ---------------------------------------------------------
elif modulo == "📦 Inventario de Producto Terminado":
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

# ---------------------------------------------------------
# MÓDULO 2: MATERIA PRIMA (OPERATIVO PURO)
# ---------------------------------------------------------
elif modulo == "🌾 Materia Prima (Físico y Movimientos)":
    st.header("🌾 Materias Primas e Empaques (Existencias Físicas)")
    st.caption("Consulta exclusiva del stock físico y la bitácora de movimientos.")

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

# ---------------------------------------------------------
# MÓDULO 3: COMPRAS E INGRESO DE INSUMOS
# ---------------------------------------------------------
elif modulo == "🛒 Compras e Ingreso de Insumos":
    st.header("🛒 Registrar Compra de Materia Prima / Empaques")
    st.caption("Ingresa las nuevas compras. El costo promedio ponderado se recalculará automáticamente.")

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

# ---------------------------------------------------------
# MÓDULO 4: REGISTRO DE LOTE Y COSTOS DIRECTOS COMPLETO
# ---------------------------------------------------------
elif modulo == "🏭 Registrar Lote de Producción y Costos":
    st.header("⚙️ Registro de Lote de Producción y Costos Directos")
    st.caption("Calcula el costo total en dinero del lote (Materia Prima + Empaques + Mano de Obra + Gas) antes de procesar el inventario.")

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

    # CÁLCULO PREVIO EN DINERO USANDO COSTOS PROMEDIO
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
    st.subheader("💰 Resumen Previo de Costos del Lote (Antes de Confirmar)")

    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    col_res1.metric("Materia Prima Directa", f"${tot_mp_dinero:.2f}")
    col_res2.metric("Empaques y Etiquetas", f"${tot_empaques_dinero:.2f}")
    col_res3.metric("Mano de Obra y Gas", f"${costo_total_mod + costo_gas_lote:.2f}")
    col_res4.metric("Costo Total en Dinero", f"${costo_total_lote_dinero:.2f}")

    st.info(f"💡 **Costo Promedio Real Directo por Paquete:** **${costo_promedio_por_bolsa:.2f} / paquete** para un total de **{total_pkts_general} paquetes**.")

    if st.button("🚀 Procesar Lote: Descontar Inventarios y Registrar Costos"):
        if total_pkts_general > 0:
            f_act = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Descuentos de MP
            st.session_state['inventario_mp']["Maíz"]["cant_kg"] -= maiz_real
            st.session_state['inventario_mp']["Aceite"]["cant_l"] -= aceite_real
            if flavacol_real_g > 0: st.session_state['inventario_mp']["Flavacol"]["cant_g"] -= flavacol_real_g
            if saz_ched_real > 0: st.session_state['inventario_mp']["Sazonador Cheddar"]["cant_g"] -= saz_ched_real
            if saz_qjal_real > 0: st.session_state['inventario_mp']["Sazonador Queso Jalapeño"]["cant_g"] -= saz_qjal_real
            if saz_hab_real > 0: st.session_state['inventario_mp']["Sazonador Habanero"]["cant_g"] -= saz_hab_real
            if saz_ado_real > 0: st.session_state['inventario_mp']["Sazonador Adobo"]["cant_g"] -= saz_ado_real

            # Descuento Empaques
            st.session_state['inventario_indirectos']["Bolsas Celofán 20x35 (pzs)"]["cant"] -= bolsas_reales
            if up_trad > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Tradicional (pzs)"]["cant"] -= up_trad
            if up_ched > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Cheddar (pzs)"]["cant"] -= up_ched
            if up_qjal > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Queso Jalapeño (pzs)"]["cant"] -= up_qjal
            if up_hab > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Habanero (pzs)"]["cant"] -= up_hab
            if up_ado > 0: st.session_state['inventario_indirectos']["Etiquetas 120g Adobo (pzs)"]["cant"] -= up_ado
            if up_65g > 0: st.session_state['inventario_indirectos']["Etiquetas 65g (pzs)"]["cant"] -= up_65g

            # Entrada Producto Terminado
            st.session_state['inventario_pt']["Tradicional (120g)"]["cant"] += up_trad
            st.session_state['inventario_pt']["Cheddar (120g)"]["cant"] += up_ched
            st.session_state['inventario_pt']["Queso Jalapeño (120g)"]["cant"] += up_qjal
            st.session_state['inventario_pt']["Habanero (120g)"]["cant"] += up_hab
            st.session_state['inventario_pt']["Adobado (120g)"]["cant"] += up_ado
            st.session_state['inventario_pt']["Pedido Especial (65g)"]["cant"] += up_65g

            # Historial
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
            st.success(f"✅ ¡Lote procesado! Costo total del lote: ${costo_total_lote_dinero:.2f} | Costo por paquete: ${costo_promedio_por_bolsa:.2f}")

# ---------------------------------------------------------
# MÓDULO 5: PUNTO DE VENTA Y MARGEN DE GANANCIA
# ---------------------------------------------------------
elif modulo == "🛍️ Punto de Venta y Margen de Ganancia":
    st.header("🛍️ Registro de Ventas a Distribuidores y Margen Bruto")
    st.caption("Verifica el margen de contribución real de cada venta restando el costo directo de producción.")

    sabor_venta = st.selectbox("Selecciona Producto / Sabor", list(st.session_state['inventario_pt'].keys()))
    stock_disp = st.session_state['inventario_pt'][sabor_venta]['cant']
    precio_u = st.session_state['inventario_pt'][sabor_venta]['precio_dist']
    costo_dir_u = st.session_state['inventario_pt'][sabor_venta].get('costo_directo_u', 5.50)

    margen_u = precio_u - costo_dir_u
    pct_margen = (margen_u / precio_u) * 100 if precio_u > 0 else 0

    col_info1, col_info2, col_info3 = st.columns(3)
    col_info1.info(f"📦 Disponible: **{stock_disp} pkts**")
    col_info2.success(f"💵 Precio Distribuidor: **${precio_u:.2f}**")
    col_info3.warning(f"📊 Margen Bruto Unitario: **${margen_u:.2f} ({pct_margen:.1f}%)**")

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
            st.success(f"✅ ¡Venta registrada! Se descontaron {cant_vender} pkts de {sabor_venta}. Ganancia generada: ${ganancia_bruta_total:.2f}")

# ---------------------------------------------------------
# MÓDULO 6: COSTOS PROMEDIO, BOM Y VALUACIÓN
# ---------------------------------------------------------
elif modulo == "💰 Costos Promedio, BOM y Valuación":
    st.header("💰 Módulo Financiero: Costos Promedio y BOM por Receta")
    st.caption("Estructura de costos unitarios de insumos y evaluación de Lista de Materiales (BOM).")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("🌾 Costos Promedio - Materia Prima Directa")
        filas_c_mp = []
        tot_val_mp = 0.0

        for k, v in st.session_state['inventario_mp'].items():
            if "cant_kg" in v:
                cant = v['cant_kg']
                costo_u = v['costo_promedio_kg']
                val_total = cant * costo_u
                filas_c_mp.append({"Insumo": k, "Stock": f"{cant:.2f} kg", "Costo Promedio": f"${costo_u:.2f} / kg", "Valor Retenido": f"${val_total:.2f}"})
            elif "cant_l" in v:
                cant = v['cant_l']
                costo_u = v['costo_promedio_l']
                val_total = cant * costo_u
                filas_c_mp.append({"Insumo": k, "Stock": f"{cant:.2f} L", "Costo Promedio": f"${costo_u:.2f} / L", "Valor Retenido": f"${val_total:.2f}"})
            else:
                cant_kg = v['cant_g'] / 1000.0
                costo_u = v['costo_promedio_kg']
                val_total = cant_kg * costo_u
                filas_c_mp.append({"Insumo": k, "Stock": f"{v['cant_g']:.0f} g", "Costo Promedio": f"${costo_u:.2f} / kg", "Valor Retenido": f"${val_total:.2f}"})
            
            tot_val_mp += val_total

        st.dataframe(pd.DataFrame(filas_c_mp), use_container_width=True, hide_index=True)
        st.metric("Total Invertido en Materia Prima", f"${tot_val_mp:.2f}")

    with col_c2:
        st.subheader("📦 Costos Unitarios - Empaques e Indirectos")
        filas_c_ind = []
        tot_val_ind = 0.0

        for k, v in st.session_state['inventario_indirectos'].items():
            cant = v['cant']
            costo_u = v['costo_u']
            val_total = cant * costo_u
            filas_c_ind.append({"Material": k, "Stock": f"{cant} pzs", "Costo Unitario": f"${costo_u:.2f} / pza", "Valor Retenido": f"${val_total:.2f}"})
            tot_val_ind += val_total

        st.dataframe(pd.DataFrame(filas_c_ind), use_container_width=True, hide_index=True)
        st.metric("Total Invertido en Empaques", f"${tot_val_ind:.2f}")

# ---------------------------------------------------------
# MÓDULO 7: CONTROL DE MERMAS Y DIFERENCIAS
# ---------------------------------------------------------
elif modulo == "⚠️ Control de Mermas y Diferencias":
    st.header("📋 Historial de Mermas y Desperdicios")
    st.caption("Bitácora de paquetes o materias primas mermadas o tiradas.")

    if len(st.session_state['historial_mermas']) > 0:
        st.dataframe(pd.DataFrame(st.session_state['historial_mermas']), use_container_width=True, hide_index=True)
    else:
        st.info("👌 No hay mermas registradas por el momento.")
